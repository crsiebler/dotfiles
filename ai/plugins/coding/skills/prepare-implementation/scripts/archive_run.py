#!/usr/bin/env python3
"""Archive a declared, verified completed run (Python 3.11+, Git, POSIX)."""

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys


LIMIT = 2 * 1024 * 1024
MANIFEST_KEYS = {
    'version', 'run_id', 'feature', 'adapter', 'task_source', 'prds',
    'journal', 'memory', 'archive_on_completion',
}


class Refusal(Exception):
    pass


def require(condition, message):
    if not condition:
        raise Refusal(message)


def relative(value):
    require(isinstance(value, str) and value and '\\' not in value,
            'invalid project-relative path')
    path = PurePosixPath(value)
    require(not path.is_absolute() and all(part not in ('', '.', '..')
            for part in value.split('/')), 'invalid project-relative path')
    require(path.parts[0] not in ('.git', 'archive') and
            all(not part.startswith('.') for part in path.parts),
            'reserved or hidden source path')
    return value


class Project:
    """Anchor filesystem operations to nonsymlink directory descriptors."""

    def __init__(self, root):
        self.root = Path(root).absolute()
        require(self.root == self.root.resolve() and self.root.is_dir(),
                'project must be an existing nonsymlink absolute directory')
        self.fd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)

    def close(self):
        os.close(self.fd)

    @contextmanager
    def parent(self, name, create=False):
        parts = PurePosixPath(name).parts
        require(parts and not PurePosixPath(name).is_absolute() and
                all(part not in ('.', '..') for part in parts), 'unsafe path')
        fd = os.dup(self.fd)
        try:
            for part in parts[:-1]:
                if create:
                    try:
                        os.mkdir(part, mode=0o700, dir_fd=fd)
                    except FileExistsError:
                        pass
                next_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                  dir_fd=fd)
                os.close(fd)
                fd = next_fd
            yield fd, parts[-1]
        finally:
            os.close(fd)

    def read(self, name, optional=False):
        try:
            with self.parent(name) as (fd, leaf):
                file_fd = os.open(leaf, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                                  dir_fd=fd)
                with os.fdopen(file_fd, 'rb') as stream:
                    require(stat.S_ISREG(os.fstat(stream.fileno()).st_mode),
                            'source must be a regular file')
                    data = stream.read(LIMIT + 1)
                    require(len(data) <= LIMIT, 'file exceeds 2 MiB limit')
                    return data
        except FileNotFoundError:
            if optional:
                return None
            raise Refusal('required file is missing') from None

    def write_new(self, name, data):
        require(len(data) <= LIMIT, 'output exceeds 2 MiB limit')
        with self.parent(name) as (fd, leaf):
            file_fd = os.open(leaf, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                              0o600, dir_fd=fd)
            with os.fdopen(file_fd, 'wb') as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.fsync(fd)

    def mkdir(self, name):
        with self.parent(name, create=True) as (fd, leaf):
            os.mkdir(leaf, mode=0o700, dir_fd=fd)
            os.fsync(fd)

    def unlink_verified(self, name, data):
        with self.parent(name) as (fd, leaf):
            file_fd = os.open(leaf, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                              dir_fd=fd)
            with os.fdopen(file_fd, 'rb') as stream:
                info = os.fstat(stream.fileno())
                require(stat.S_ISREG(info.st_mode) and stream.read(LIMIT + 1) == data,
                        'source changed before removal; reconcile partial archive')
            latest = os.stat(leaf, dir_fd=fd, follow_symlinks=False)
            require((latest.st_dev, latest.st_ino, latest.st_mtime_ns, latest.st_size)
                    == (info.st_dev, info.st_ino, info.st_mtime_ns, info.st_size),
                    'source replaced before removal; reconcile partial archive')
            os.unlink(leaf, dir_fd=fd)
            os.fsync(fd)

    def entries(self, name):
        with self.parent(name + '/entry') as (fd, _):
            names = os.listdir(fd)
            require(len(names) <= 1000, 'archive directory exceeds inspection limit')
            return [(value, os.stat(value, dir_fd=fd, follow_symlinks=False))
                    for value in names]


def decode(data):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    try:
        return json.loads(data, object_pairs_hook=unique)
    except (ValueError, UnicodeError, TypeError):
        raise Refusal('invalid JSON') from None


def blocks(data, language):
    try:
        content = data.decode('utf-8')
    except UnicodeError:
        raise Refusal('invalid UTF-8 document') from None
    pattern = rf'^```{re.escape(language)}\r?\n(.*?)\r?\n```[ \t]*\r?$'
    found = re.findall(pattern, content, re.M | re.S)
    require(len(found) <= 1000, 'too many structured records')
    require(len(found) == len(re.findall(rf'^```{re.escape(language)}[ \t]*\r?$', content, re.M)),
            'malformed structured block')
    return [decode(value) for value in found]


def manifest_read(data, prd):
    found = blocks(data, 'work-run')
    require(len(found) == 1, 'PRD requires exactly one work-run JSON block')
    value = found[0]
    require(isinstance(value, dict) and set(value) == MANIFEST_KEYS and
            type(value['version']) is int and value['version'] == 1,
            'invalid version-1 run manifest')
    for key in ('run_id', 'feature'):
        require(isinstance(value[key], str) and
                re.fullmatch(r'[a-z0-9][a-z0-9-]{0,79}', value[key]),
                'run ID and feature must be lowercase path-safe identifiers')
    require(value['archive_on_completion'] is True, 'automatic archival is disabled')
    require(value['adapter'] in ('CodexGoalMarkdown', 'RalphJSON'), 'unknown adapter')
    relative(value['task_source'])
    require(value['task_source'].endswith('.md' if value['adapter'] == 'CodexGoalMarkdown'
                                         else '.json'), 'task source does not match adapter')
    require(value['journal'] == 'progress.md' and value['memory'] == 'memory.json',
            'journal and memory must use root progress.md and memory.json')
    prds = value['prds']
    require(isinstance(prds, list) and 1 <= len(prds) <= 32 and
            all(isinstance(path, str) for path in prds) and len(set(prds)) == len(prds),
            'invalid PRD inventory')
    for path in prds:
        relative(path)
        require(path.endswith('.md'), 'PRDs must be Markdown files')
    require(prd in prds, 'invoked PRD is not declared in the run')
    paths = [value['task_source'], value['journal'], value['memory'], *prds]
    names = [PurePosixPath(path).name.casefold() for path in paths]
    require(len(set(names)) == len(names) and '_archive.json' not in names,
            'flat archive filename collision')
    return value


def tasks_read(data, adapter):
    if adapter == 'RalphJSON':
        value = decode(data)
        require(isinstance(value, dict) and isinstance(value.get('userStories'), list),
                'invalid Ralph task source')
        stories = value['userStories']
        require(all(isinstance(story, dict) for story in stories), 'invalid Ralph story')
        tasks = [(story.get('id'), story.get('passes') is True) for story in stories]
    else:
        try:
            content = data.decode('utf-8')
        except UnicodeError:
            raise Refusal('invalid Markdown task source') from None
        # Only the top-level story completion marker, not nested acceptance boxes.
        sections = re.findall(r'^### (US-[0-9]+) - [^\n]+\n(.*?)(?=^### |^## |\Z)',
                              content, re.M | re.S)
        tasks = []
        for story_id, section in sections:
            markers = re.findall(r'^- \[([ xX])\] Story complete[ \t]*\r?$', section, re.M)
            require(len(markers) == 1, 'story needs one explicit completion marker')
            tasks.append((story_id, markers[0].lower() == 'x'))
    require(tasks and len(tasks) <= 1000 and
            all(isinstance(story_id, str) and re.fullmatch(r'US-[0-9]+', story_id)
                for story_id, _ in tasks), 'invalid or empty story inventory')
    require(len({story_id for story_id, _ in tasks}) == len(tasks), 'duplicate story ID')
    return dict(tasks)


def results_read(data, manifest):
    found = blocks(data, 'story-result')
    records = {}
    for value in found:
        require(isinstance(value, dict) and type(value.get('version')) is int and
                value['version'] == 1 and value.get('run_id') == manifest['run_id'] and
                isinstance(value.get('story_id'), str), 'foreign or invalid story record')
        records[value['story_id']] = value
    return records


def evidence_check(record, adapter):
    checks = record.get('checks')
    require(isinstance(checks, list) and checks and len(checks) <= 100,
            'story requires structured check evidence')
    for check in checks:
        require(isinstance(check, dict) and
                check.get('status') in ('passed', 'not_applicable') and
                all(isinstance(check.get(key), str) and check[key].strip()
                    for key in ('command', 'evidence')), 'failed or unavailable required check')
    review = record.get('review')
    require(isinstance(review, dict) and review.get('verdict') == 'pass' and
            isinstance(review.get('evidence'), str) and review['evidence'].strip(),
            'missing passing review evidence')
    if review.get('kind') == 'native':
        role = 'story-reviewer' if adapter == 'CodexGoalMarkdown' else 'ralph-reviewer'
        require(review.get('role') == role and isinstance(review.get('session_id'), str)
                and review['session_id'].strip(), 'missing required reviewer provenance')
    else:
        require(review.get('kind') == 'self' and isinstance(review.get('reason'), str)
                and review['reason'].strip(), 'self-review requires its budget/risk reason')


def memory_check(data):
    value = decode(data)
    require(isinstance(value, dict) and set(value) == {'version', 'patterns', 'suppressions'}
            and type(value['version']) is int and value['version'] == 1 and
            all(isinstance(value[key], list) and len(value[key]) <= 20
                for key in ('patterns', 'suppressions')), 'invalid bounded memory')
    specifications = {
        'patterns': {'id', 'lens', 'scope', 'guidance', 'evidence_count', 'accepted_count',
                     'rejected_count', 'last_validated_story', 'status'},
        'suppressions': {'fingerprint', 'reason', 'scope', 'last_reviewed_story'},
    }
    for group, keys in specifications.items():
        identifiers = set()
        for item in value[group]:
            require(isinstance(item, dict) and set(item) == keys, 'invalid memory entry fields')
            strings = keys - {'scope', 'evidence_count', 'accepted_count', 'rejected_count'}
            require(all(isinstance(item[key], str) and item[key].strip() for key in strings),
                    'invalid memory entry strings')
            scopes = item['scope']
            require(isinstance(scopes, list) and scopes and
                    all(isinstance(scope, str) and scope for scope in scopes),
                    'invalid memory scope')
            for scope in scopes:
                require(not PurePosixPath(scope).is_absolute() and '\\' not in scope and
                        '..' not in scope.split('/'), 'invalid project-relative memory scope')
            identifier = item['id'] if group == 'patterns' else item['fingerprint']
            require(identifier not in identifiers, 'duplicate memory identifier')
            identifiers.add(identifier)
            if group == 'patterns':
                require(item['lens'] in ('correctness', 'qa', 'security', 'ui', 'ux') and
                        item['status'] == 'active' and
                        all(type(item[key]) is int and item[key] >= 0 for key in
                            ('evidence_count', 'accepted_count', 'rejected_count')) and
                        item['accepted_count'] >= 1 and item['evidence_count'] ==
                        item['accepted_count'] + item['rejected_count'], 'invalid memory counters')


def git(root, *args, optional=False):
    process = subprocess.run(['git', '--no-optional-locks', '-C', str(root), *args],
                             capture_output=True)
    require(optional or process.returncode == 0, 'Git evidence is unavailable')
    require(len(process.stdout) <= LIMIT, 'Git evidence exceeds inspection limit')
    return process


def delivery(project, manifest, files):
    require(git(project.root, 'rev-parse', '--show-toplevel').stdout.decode().strip()
            == str(project.root), 'project must be the Git worktree root')
    head = git(project.root, 'rev-parse', 'HEAD').stdout.decode().strip()
    for path, data in files.items():
        committed = git(project.root, 'show', f'{head}:{path}', optional=True)
        require(committed.returncode == 0 and committed.stdout == data,
                'active run files must match their committed contents')
    staged = git(project.root, 'diff', '--cached', '--quiet', '--', *files, optional=True)
    require(staged.returncode == 0, 'run artifacts have staged changes')
    task_path = manifest['task_source']
    tasks = tasks_read(files[task_path], manifest['adapter'])
    require(all(tasks.values()), 'run has incomplete stories')
    records = results_read(files['progress.md'], manifest)
    require(set(records) == set(tasks), 'story evidence does not match task inventory')
    for record in records.values():
        evidence_check(record, manifest['adapter'])
    revisions = git(project.root, 'log', '-n', '1001', '--reverse', '--format=%H',
                    '--', task_path, 'progress.md').stdout.decode().splitlines()
    require(len(revisions) <= 1000, 'delivery history exceeds inspection limit')
    commits = {}
    for revision in revisions:
        plan = git(project.root, 'show', f'{revision}:{task_path}', optional=True)
        journal = git(project.root, 'show', f'{revision}:progress.md', optional=True)
        if plan.returncode or journal.returncode:
            continue
        try:
            historical_tasks = tasks_read(plan.stdout, manifest['adapter'])
            historical_records = results_read(journal.stdout, manifest)
        except Refusal:
            # Earlier runs/legacy documents at the same paths are not this run's
            # evidence. The current documents were validated above.
            continue
        for story_id, record in records.items():
            if story_id not in commits and historical_tasks.get(story_id) and \
                    historical_records.get(story_id) == record:
                commits[story_id] = revision
        if len(commits) == len(tasks):
            break
    require(set(commits) == set(tasks), 'committed story delivery evidence is missing')
    branch = git(project.root, 'symbolic-ref', '--quiet', '--short', 'HEAD', optional=True)
    return head, branch.stdout.decode().strip() or None, [
        {'id': story_id, 'commit': commits[story_id], 'result': records[story_id]}
        for story_id in tasks]


@contextmanager
def runner_guard(project, adapter, task_data):
    require(project.read('.ralph-stop', optional=True) is None, 'stop file blocks archival')
    lock_fd = None
    try:
        control = git(project.root, 'rev-parse', '--git-path', 'ralph').stdout.decode().strip()
        control_path = Path(control)
        if not control_path.is_absolute():
            control_path = project.root / control_path
        if control_path.exists() or control_path.is_symlink():
            require(control_path == control_path.resolve() and control_path.is_dir(),
                    'unsafe Ralph control directory')
            lock_path = control_path / 'lock'
            if lock_path.exists() or lock_path.is_symlink():
                lock_fd = os.open(lock_path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
                require(stat.S_ISREG(os.fstat(lock_fd).st_mode), 'invalid Ralph lock')
                try:
                    fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    raise Refusal('Ralph runner is still active') from None
            state_path = control_path / 'state.json'
            if state_path.exists() or state_path.is_symlink():
                fd = os.open(state_path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
                with os.fdopen(fd, 'rb') as stream:
                    require(stat.S_ISREG(os.fstat(stream.fileno()).st_mode), 'unsafe runner state')
                    data = stream.read(LIMIT + 1)
                    require(len(data) <= LIMIT, 'runner state exceeds limit')
                state = decode(data)
                require(isinstance(state, dict) and type(state.get('version')) is int and
                        state['version'] == 1 and state.get('status') == 'completed',
                        'unresolved runner state blocks archival')
                if adapter == 'RalphJSON':
                    require(state.get('expected_plan') == decode(task_data),
                            'Ralph completion state belongs to another plan')
                for key in ('runner_pid', 'child_pid'):
                    pid = state.get(key)
                    if type(pid) is int and pid > 0:
                        try:
                            os.kill(pid, 0)
                        except ProcessLookupError:
                            continue
                        raise Refusal('recorded runner process is still alive')
            else:
                require(adapter != 'RalphJSON', 'Ralph completion state is missing')
        else:
            require(adapter != 'RalphJSON', 'Ralph completion state is missing')
        yield
    finally:
        if lock_fd is not None:
            os.close(lock_fd)


@contextmanager
def archive_lock(project):
    # Git resolves a separate metadata path for each linked worktree.
    path = Path(git(project.root, 'rev-parse', '--git-path',
                    'archive-run.lock').stdout.decode().strip())
    if not path.is_absolute():
        path = project.root / path
    metadata = Project(path.parent)
    lock_fd = None
    try:
        with metadata.parent(path.name) as (fd, leaf):
            lock_fd = os.open(leaf, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK,
                              0o600, dir_fd=fd)
        require(stat.S_ISREG(os.fstat(lock_fd).st_mode), 'unsafe archive lock')
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise Refusal('another archive writer is active') from None
        yield
    finally:
        if lock_fd is not None:
            os.close(lock_fd)
        metadata.close()


def inventory(files):
    return [{'source': path, 'name': PurePosixPath(path).name,
             'sha256': hashlib.sha256(data).hexdigest(), 'size': len(data)}
            for path, data in files.items()]


def existing_archive(project, prd, run_id=None):
    try:
        entries = project.entries('archive')
    except FileNotFoundError:
        return None
    matches = []
    for name, info in entries:
        if not stat.S_ISDIR(info.st_mode) or name.startswith('.'):
            continue
        directory = 'archive/' + name
        raw = project.read(directory + '/_archive.json', optional=True)
        if raw is None:
            continue
        receipt = decode(raw)
        require(isinstance(receipt, dict), 'invalid archive receipt')
        matches_run = (receipt.get('run_id') == run_id if run_id is not None
                       else receipt.get('source_prd') == prd)
        if matches_run:
            matches.append((directory, receipt))
    require(len(matches) <= 1, 'ambiguous prior archive; specify --run-id')
    if not matches:
        return None
    directory, receipt = matches[0]
    require(receipt.get('version') == 1 and receipt.get('status') == 'archived',
            'partial archive requires reconciliation; automatic cleanup is refused')
    items = receipt.get('files')
    require(isinstance(items, list) and 3 <= len(items) <= 35, 'invalid archive inventory')
    for item in items:
        require(isinstance(item, dict), 'invalid archive item')
        source = relative(item.get('source'))
        require(item.get('name') == PurePosixPath(source).name, 'invalid archive filename')
        data = project.read(directory + '/' + item['name'])
        require(hashlib.sha256(data).hexdigest() == item.get('sha256') and
                len(data) == item.get('size'), 'archive verification failed')
        require(project.read(source, optional=True) is None,
                'archived run has active copies; reconcile without automatic removal')
    return {'status': 'already_archived', 'destination': directory,
            'run_id': receipt['run_id'], 'files': items}


def execute(project, prd, dry_run, run_id=None):
    relative(prd)
    primary = project.read(prd, optional=True)
    if primary is None:
        prior = existing_archive(project, prd, run_id)
        require(prior is not None, 'PRD is missing and no verified archive matches')
        return prior
    manifest = manifest_read(primary, prd)
    require(run_id is None or run_id == manifest['run_id'], 'run ID does not match PRD')
    prior = existing_archive(project, prd, manifest['run_id'])
    if prior:
        return prior
    paths = [*manifest['prds'], manifest['task_source'], 'progress.md']
    files = {path: project.read(path) for path in paths}
    for path in manifest['prds']:
        require(manifest_read(files[path], path) == manifest, 'PRDs disagree on run ownership')
    memory = project.read('memory.json', optional=True)
    if memory is not None:
        memory_check(memory)
        files['memory.json'] = memory
    with runner_guard(project, manifest['adapter'], files[manifest['task_source']]):
        head, branch, stories = delivery(project, manifest, files)
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%S%fZ')
        directory = f'archive/{timestamp}-{manifest["feature"]}'
        items = inventory(files)
        result = {'status': 'preview' if dry_run else 'archived', 'run_id': manifest['run_id'],
                  'destination': directory, 'files': items, 'stories': stories,
                  'head': head, 'branch': branch}
        if dry_run:
            return result
        # One archive writer per worktree; never reset/delete its metadata lock.
        with archive_lock(project):
            require(existing_archive(project, prd, manifest['run_id']) is None,
                    'run was archived concurrently')
            staging = 'archive/.pending-' + manifest['run_id']
            project.mkdir(staging)
            receipt = {'version': 1, 'status': 'preserved', 'run_id': manifest['run_id'],
                       'source_prd': prd, 'manifest': manifest, 'head': head, 'branch': branch,
                       'stories': stories, 'files': items, 'destination': directory}
            for item in items:
                project.write_new(staging + '/' + item['name'], files[item['source']])
            project.write_new(staging + '/_archive.json',
                              json.dumps(receipt, indent=2).encode() + b'\n')
            for item in items:
                require(project.read(staging + '/' + item['name']) == files[item['source']],
                        'copy verification failed; sources preserved')
            require(git(project.root, 'rev-parse', 'HEAD').stdout.decode().strip() == head and
                    all(project.read(path) == data for path, data in files.items()),
                    'active run changed; sources preserved')
            # mkdir reserves the final name without replacing any existing directory.
            project.mkdir(directory)
            with project.parent(staging + '/entry') as (src_fd, _):
                with project.parent(directory + '/entry') as (dst_fd, _):
                    for name in [item['name'] for item in items] + ['_archive.json']:
                        os.rename(name, name, src_dir_fd=src_fd, dst_dir_fd=dst_fd)
                    os.fsync(src_fd)
                    os.fsync(dst_fd)
            with project.parent(staging) as (fd, leaf):
                os.rmdir(leaf, dir_fd=fd)
                os.fsync(fd)
            # Verify the complete published archive and all sources before any removal.
            require(all(project.read(directory + '/' + item['name']) == files[item['source']]
                        for item in items) and
                    all(project.read(path) == data for path, data in files.items()) and
                    git(project.root, 'rev-parse', 'HEAD').stdout.decode().strip() == head and
                    git(project.root, 'diff', '--cached', '--quiet', '--', *files,
                        optional=True).returncode == 0,
                    'published archive or sources changed; cleanup refused')
            for path, data in files.items():
                project.unlink_verified(path, data)
            receipt['status'] = 'archived'
            project.write_new(directory + '/_receipt.pending',
                              json.dumps(receipt, indent=2).encode() + b'\n')
            with project.parent(directory + '/_archive.json') as (fd, leaf):
                os.replace('_receipt.pending', leaf, src_dir_fd=fd, dst_dir_fd=fd)
                os.fsync(fd)
            return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True, help='absolute Git worktree root')
    parser.add_argument('--prd', required=True, help='declared project-relative PRD path')
    parser.add_argument('--run-id', help='disambiguate a repeated invocation after PRD removal')
    parser.add_argument('--dry-run', action='store_true', help='validate and preview without writes')
    args = parser.parse_args()
    project = None
    try:
        project = Project(args.project)
        result = execute(project, args.prd, args.dry_run, args.run_id)
        print(json.dumps(result))
        return 0
    except (Refusal, OSError) as error:
        # Never print source contents, subprocess stderr, or credential-bearing paths.
        reason = str(error) if isinstance(error, Refusal) else 'filesystem operation failed'
        print(json.dumps({'status': 'blocked', 'reason': reason,
                          'recovery': 'Preserve sources and any archive; inspect partial state before retrying.'}))
        return 2
    finally:
        if project is not None:
            project.close()


if __name__ == '__main__':
    sys.exit(main())
