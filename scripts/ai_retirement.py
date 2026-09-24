"""Exact-tree ownership and retirement for repository-managed AI installations."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import stat
import uuid

NAME = re.compile(r'[a-z0-9][a-z0-9-]*\Z')

# Full trees from d92e46b^, not a name-only deletion allowlist. Unknown legacy
# versions (including use-exa, absent from this checkout's history) stay manual.
LEGACY = {'analyze-review-feedback': [{
    'SKILL.md': 'c4c7ad721c3de4df0a76f6136e8467fe14c9a3708ea8c83e2d166c7cca5b59db',
    'references/': 'directory',
    'references/github.md': '0d44847f5d1fb6b02250562d7088d5f1aa325e92f184879c99b5ba07aac5e4aa',
}]}


def safe(path):
    if any(p.is_symlink() for p in [path, *path.parents]):
        raise ValueError(f'retirement path uses a symlink: {path}')


def fingerprint(directory):
    safe(directory)
    if not directory.is_dir():
        raise ValueError(f'not a skill/plugin directory: {directory}')
    result = {}
    for path in sorted(directory.rglob('*')):
        safe(path)
        mode = path.stat().st_mode
        if stat.S_ISREG(mode):
            result[path.relative_to(directory).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        elif stat.S_ISDIR(mode):
            result[path.relative_to(directory).as_posix() + '/'] = 'directory'
        else:
            raise ValueError(f'unsupported retirement asset: {path}')
    return result


def skill_copy_fingerprint(directory):
    """Expected copy payload for skills CLI 1.5.24, applied to sources only.

    Its copyDirectory excludes metadata.json entries and .git, __pycache__,
    and __pypackages__ directories. Installed trees and retirement candidates
    still use the complete fingerprint so extra/custom files stay protected.
    """
    result = {}
    excluded_dirs = {'.git', '__pycache__', '__pypackages__'}
    for relative, digest in fingerprint(directory).items():
        parts = Path(relative).parts
        directories = parts if digest == 'directory' else parts[:-1]
        if 'metadata.json' in parts or excluded_dirs.intersection(directories):
            continue
        result[relative] = digest
    return result


def valid_tree(tree):
    return isinstance(tree, dict) and bool(tree) and all(
        isinstance(p, str) and p and not Path(p).is_absolute()
        and '..' not in Path(p).parts and isinstance(h, str)
        and (re.fullmatch(r'[0-9a-f]{64}', h) or (p.endswith('/') and h == 'directory'))
        for p, h in tree.items())


def load(path, root, kind):
    safe(path)
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
        if (data['version'] != 1 or data['root'] != str(root.resolve())
                or data['kind'] != kind or not isinstance(data['entries'], dict)):
            raise ValueError()
        return data['entries']
    except (ValueError, KeyError, TypeError):
        raise ValueError(f'invalid or foreign installation inventory: {path}') from None


def save(path, root, kind, entries):
    safe(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.' + uuid.uuid4().hex)
    try:
        with temp.open('x') as stream:
            json.dump({'version': 1, 'root': str(root.resolve()), 'kind': kind,
                       'entries': entries}, stream, indent=2)
            stream.write('\n')
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)


def archive(source, target, expected, move=False):
    if fingerprint(source) != expected:
        raise ValueError(f'retirement candidate changed after preflight: {source}')
    safe(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)
    if fingerprint(target) != expected or fingerprint(source) != expected:
        raise ValueError(f'retirement backup verification failed: {source}')
    if move:
        shutil.rmtree(source)


def stamp():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '-' + uuid.uuid4().hex[:8]


class Skills:
    def __init__(self, root, target, shared, desired, legacy=None, agent='opencode', lock_path=None):
        self.root, self.target, self.shared = root, target, shared
        self.agent, self.desired = agent, desired
        self.legacy = LEGACY if legacy is None else legacy
        self.state_path = target / '.install-ai-skills.json'
        self.lock_path = lock_path or shared.parent / '.skill-lock.json'
        if not self.lock_path.is_absolute():
            raise ValueError('XDG_STATE_HOME must be absolute for skill retirement')
        self.retired, self.conflicts, self.pending = {}, [], set()
        self.previous = {}

    def read_lock(self):
        safe(self.lock_path)
        if not self.lock_path.exists():
            return None
        try:
            data = json.loads(self.lock_path.read_text())
            if (data['version'] != 3 or not isinstance(data['skills'], dict)
                    or not all(isinstance(v, dict) for v in data['skills'].values())):
                raise ValueError()
            return data
        except (ValueError, KeyError, TypeError):
            raise ValueError(f'invalid or unsupported skills CLI lock: {self.lock_path}') from None

    def prepare(self):
        self.retired, self.conflicts, self.pending = {}, [], set()
        self.previous = load(self.state_path, self.root, 'skills')
        for name, trees in self.previous.items():
            if not NAME.fullmatch(name) or not isinstance(trees, list) or not all(valid_tree(t) for t in trees):
                raise ValueError(f'invalid skill installation inventory: {self.state_path}')
        candidates = dict(self.legacy)
        for name, trees in self.previous.items():
            candidates[name] = [*candidates.get(name, []), *trees]
        for name, trees in candidates.items():
            if name in self.desired:
                continue
            found = {}
            conflict = False
            for base in dict.fromkeys([self.target / 'skills', self.shared]):
                path = base / name
                if not path.exists() and not path.is_symlink():
                    continue
                try:
                    actual = fingerprint(path)
                    if actual not in trees:
                        raise ValueError('unverified content')
                    found[path] = actual
                except ValueError:
                    self.conflicts.append(path)
                    conflict = True
            # A CLI call may affect both roots: never partially select a name.
            if not conflict:
                self.retired.update(found)
                if found or name in self.previous:
                    self.pending.add(name)
        if self.pending:
            self.read_lock()

    def apply(self, execute):
        for path, tree in self.retired.items():
            if fingerprint(path) != tree:
                raise ValueError(f'retirement candidate changed after preflight: {path}')
        # Preserve pending names before any removal, including legacy bootstrap.
        entries = dict(self.previous)
        for path, tree in self.retired.items():
            entries.setdefault(path.name, [])
            if tree not in entries[path.name]:
                entries[path.name].append(tree)
        if self.pending:
            save(self.state_path, self.root, 'skills', entries)
        backup = self.target / '.install-ai-backups' / stamp() / 'retired'
        if self.pending and self.read_lock() is not None:
            safe(backup)
            backup.mkdir(parents=True, exist_ok=False)
            shutil.copy2(self.lock_path, backup / 'skills-lock.json')
            if (backup / 'skills-lock.json').read_bytes() != self.lock_path.read_bytes():
                raise ValueError('skills CLI lock backup verification failed')
        for path, tree in self.retired.items():
            scope = 'shared' if path.parent == self.shared else self.agent
            archive(path, backup / scope / path.name, tree, move=True)
        for name in sorted(self.pending):
            # All paths this scoped command can delete have already been
            # verified and archived. Shared removal must not depend on the CLI's
            # other-agent detection, which can retain obsolete canonical files.
            for base in [self.target / 'skills', self.shared]:
                safe(base / name)
                if (base / name).exists():
                    raise ValueError(f'retirement path reappeared: {base / name}')
            before = self.read_lock()
            execute(['skills', 'remove', name, '--global', '--agent', self.agent, '--yes'])
            after = self.read_lock()
            if before is not None:
                expected = {k: v for k, v in before['skills'].items() if k != name}
                actual = {k: v for k, v in (after or {}).get('skills', {}).items() if k != name}
                if expected != actual:
                    raise ValueError('skills CLI changed unrelated tracking; inspect retirement backup')
            if any((base / name).exists() for base in [self.target / 'skills', self.shared]):
                raise ValueError(f'skill removal did not complete: {name}')

    def record(self, verify=False):
        entries = dict(self.previous)
        for name in self.pending:
            entries.pop(name, None)
        for name, expected in self.desired.items():
            matches = []
            for base in dict.fromkeys([self.target / 'skills', self.shared]):
                path = base / name
                try:
                    if path.exists() and fingerprint(path) == expected:
                        matches.append(expected)
                except ValueError:
                    # A current same-name custom/symlinked copy is not evidence
                    # of ownership; leave it alone and track verified copies.
                    continue
            if verify and not matches:
                raise ValueError(f'installed skill not verified: {name}')
            if matches:
                trees = entries.setdefault(name, [])
                if expected not in trees:
                    trees.append(expected)
        save(self.state_path, self.root, 'skills', entries)


class Plugins:
    def __init__(self, root, target, marketplace, desired):
        self.root, self.target, self.marketplace = root, target, marketplace
        self.desired = {name: str(path.resolve()) for name, path in desired}
        self.state_path = target / '.install-ai-plugins.json'
        self.previous, self.retired, self.conflicts = {}, [], []

    def verify(self, execute):
        rows = json.loads(execute(['codex', 'plugin', 'list', '--marketplace',
                                  self.marketplace, '--json']))['installed']
        for name, source in self.desired.items():
            identifier = name + '@' + self.marketplace
            if not any(row['pluginId'] == identifier and row['source'] ==
                       {'source': 'local', 'path': source} for row in rows):
                raise ValueError(f'installed native plugin not verified: {identifier}')

    def prepare(self, installed):
        self.previous = load(self.state_path, self.root, 'plugins:' + self.marketplace)
        for name, path in self.previous.items():
            if (not NAME.fullmatch(name) or not isinstance(path, str)
                    or not Path(path).is_absolute()
                    or not Path(path).is_relative_to(self.root.resolve())):
                raise ValueError(f'invalid plugin installation inventory: {self.state_path}')
        self.retired = []
        if installed is None:
            self.retired = [name + '@' + self.marketplace for name in self.previous
                            if name not in self.desired]
            return
        for row in installed:
            identifier = row['pluginId']
            name = identifier.removesuffix('@' + self.marketplace)
            if identifier != name + '@' + self.marketplace or name not in self.previous or name in self.desired:
                continue
            if row['source'] != {'source': 'local', 'path': self.previous[name]}:
                raise ValueError(f'retired plugin source conflict: {identifier}')
            self.retired.append(identifier)

    def apply(self, execute):
        for identifier in self.retired:
            rows = json.loads(execute(['codex', 'plugin', 'list', '--marketplace',
                                      self.marketplace, '--json']))['installed']
            self.prepare(rows)
            if identifier not in self.retired:
                continue
            name = identifier.removesuffix('@' + self.marketplace)
            cache = self.target / 'plugins/cache' / self.marketplace / name
            safe(cache)
            if cache.exists():
                archive(cache, self.target / '.install-ai-backups' / stamp()
                        / 'retired/plugins' / name, fingerprint(cache))
            execute(['codex', 'plugin', 'remove', identifier])
            after = json.loads(execute(['codex', 'plugin', 'list', '--marketplace',
                                       self.marketplace, '--json']))['installed']
            if any(row['pluginId'] == identifier for row in after):
                raise ValueError(f'plugin removal did not complete: {identifier}')

    def record(self):
        # Keep recoverable source snapshots even if a later checkout removes a
        # whole bundle. Native cache management remains exclusively Codex-owned.
        for name, source in self.desired.items():
            tree = fingerprint(Path(source))
            digest = hashlib.sha256(json.dumps(tree, sort_keys=True).encode()).hexdigest()
            backup = self.target / '.install-ai-backups' / 'plugin-sources' / name / digest
            safe(backup)
            if not backup.exists():
                archive(Path(source), backup, tree)
            elif fingerprint(backup) != tree:
                raise ValueError(f'plugin source backup conflict: {backup}')
        save(self.state_path, self.root, 'plugins:' + self.marketplace, self.desired)
