"""Explicit source permission contract; no live MCP calls or credentials."""

import fnmatch
import json
from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
# Reviewed native names, not names inferred from the configuration under test.
# Rovo catalog: developer.atlassian.com/cloud/rovo-mcp/guides/supported-tools/
# PostgreSQL: crsiebler/mcp-suite commit 2a2881a5986d22349dd9fcec84820cd58656ed61.
READ_TOOLS = {
    'github': set('''
        get_commit get_file_contents get_label get_latest_release
        get_release_by_tag get_tag issue_read list_branches list_commits
        list_issue_fields list_issue_types list_issues list_pull_requests
        list_releases list_repository_collaborators list_tags pull_request_read
        search_code search_commits search_issues search_pull_requests
        search_repositories
    '''.split()),
    'jira': set('''
        atlassianUserInfo getAccessibleAtlassianResources discover
        getContentFormatGuide executeRead search getTeamworkGraphContext
        getTeamworkGraphObject getJiraIssue listJiraProjects
        listJiraProjectIssueTypesMetadata getJiraIssueTypeMetaWithFields
        listJiraIssueTransitions listJiraIssueLinkTypes listJiraIssueRemoteIssueLinks
        listJiraIssueWorklogs lookupJiraAccountId findJiraIssueAssignableUsers
        listJiraIssueComments listJiraIssueChangelogs getJiraCurrentUser getJiraUser
        listJiraStatuses listJiraProjectComponents getJiraProjectVersions
        getJiraProjectVersionRelatedWork listJiraBoards getJiraBoardConfig
        getJiraBoardIssueData getJiraBoardSprintData listJiraBoardSprints
        listJiraFilters listJiraDashboards getJiraEntityProperty
        downloadJiraIssueAttachment searchJiraIssuesUsingJql
        getJiraIssueRemoteIssueLinks getJiraProjectIssueTypesMetadata
        getIssueLinkTypes getTransitionsForJiraIssue getVisibleJiraProjects
        getConfluencePage getConfluencePageDescendants getConfluencePageFooterComments
        getConfluencePageInlineComments getConfluenceCommentChildren
        getConfluenceSpaces getPagesInConfluenceSpace searchConfluenceUsingCql
        searchAtlassian fetchAtlassian fetch
    '''.split()),
    'postgresql': {'check_dangerous_operations_allowed'},
    'exa': {'web_search_exa', 'web_search_advanced_exa', 'web_fetch_exa', 'agent_run'},
    'context7': {'resolve-library-id', 'query-docs'},
}


class MCPPermissionsTest(unittest.TestCase):
    def setUp(self):
        self.codex = tomllib.loads((ROOT / 'ai/codex/config.toml').read_text())
        self.opencode = json.loads((ROOT / 'ai/opencode/opencode.json').read_text())

    def permission(self, server, tool):
        name = f'{server}_{tool}'
        matches = [action for pattern, action in self.opencode['permission'].items()
                   if fnmatch.fnmatchcase(name, pattern)]
        self.assertTrue(matches, f'{name}: missing explicit permission')
        return matches[-1]

    def test_exact_read_allowlists_match_in_both_harnesses(self):
        for server, names in READ_TOOLS.items():
            with self.subTest(server=server):
                config = self.codex['mcp_servers'][server]
                self.assertEqual(config['default_tools_approval_mode'], 'prompt')
                approved = {name for name, settings in config.get('tools', {}).items()
                            if settings.get('approval_mode') == 'approve'}
                self.assertEqual(approved, names)
                oc = {name.removeprefix(server + '_')
                      for name, value in self.opencode['permission'].items()
                      if name.startswith(server + '_') and value == 'allow'}
                self.assertEqual(oc, names)
                for name in names:
                    self.assertEqual(self.permission(server, name), 'allow')

    def test_writes_and_unknown_tools_still_ask(self):
        mutations = {
            'github': ['issue_write', 'push_files', 'create_or_update_file',
                       'create_branch', 'update_pull_request', 'merge_pull_request',
                       'add_issue_comment', 'pull_request_review_write'],
            'jira': ['executeWrite', 'executeDestructive', 'createJiraIssue',
                     'editJiraIssue', 'addTeamworkGraphContext'],
            'postgresql': ['execute_query'],
        }
        for server, names in mutations.items():
            for name in [*names, 'future_unknown_tool']:
                with self.subTest(server=server, name=name):
                    self.assertEqual(self.permission(server, name), 'ask')
                    settings = self.codex['mcp_servers'][server]
                    self.assertEqual(settings.get('tools', {}).get(name, {}).get(
                        'approval_mode', settings['default_tools_approval_mode']), 'prompt')

    def test_research_only_and_optional_service_policy(self):
        for server in ('exa', 'context7'):
            self.assertEqual(self.permission(server, 'future_unknown_tool'), 'deny')
            self.assertEqual(set(self.codex['mcp_servers'][server]['enabled_tools']),
                             READ_TOOLS[server])
        for server in ('chrome', 'playwright', 'jam', 'elevenlabs'):
            self.assertNotIn(server, self.codex['mcp_servers'])
            self.assertIs(self.opencode['mcp'][server]['enabled'], False)
            self.assertEqual(self.permission(server, 'any_tool'),
                             'ask' if server == 'elevenlabs' else 'allow')


if __name__ == '__main__':
    unittest.main()
