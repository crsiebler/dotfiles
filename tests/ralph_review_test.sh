#!/bin/bash

set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
AGENT_FILE="$ROOT_DIR/ai/opencode/agents/ralph-reviewer.md"
RALPH_FILE="$ROOT_DIR/ai/opencode/agents/ralph.md"
REFERENCES="$ROOT_DIR/ai/plugins/coding/skills/prepare-implementation/references"
EXECUTION_FILE="$REFERENCES/story-execution.md"
REVIEW_FILE="$REFERENCES/story-review.md"

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

[[ -f "$AGENT_FILE" ]] || fail "missing ralph-reviewer agent"
[[ -f "$RALPH_FILE" ]] || fail "missing Ralph primary agent"
[[ -f "$EXECUTION_FILE" ]] || fail "missing shared execution contract"
[[ -f "$REVIEW_FILE" ]] || fail "missing shared review protocol"

ruby -e '
  require "yaml"

  path = ARGV.fetch(0)
  content = File.read(path)
  match = content.match(/\A---\s*\n(.*?)\n---\s*\n/m)
  abort "missing YAML frontmatter" unless match

  config = YAML.safe_load(match[1], permitted_classes: [], aliases: false)
  abort "Ralph agent must use primary mode" unless config["mode"] == "primary"
' "$RALPH_FILE"

ruby -e '
  require "yaml"

  path = ARGV.fetch(0)
  content = File.read(path)
  match = content.match(/\A---\s*\n(.*?)\n---\s*\n/m)
  abort "missing YAML frontmatter" unless match

  config = YAML.safe_load(match[1], permitted_classes: [], aliases: false)
  abort "agent must use subagent mode" unless config["mode"] == "subagent"
  abort "agent steps must be bounded to three" unless config["steps"] == 3

  permissions = config.fetch("permission")
  abort "all reviewer tools must default to denied" unless permissions["*"] == "deny"
  %w[read glob grep].each do |name|
    abort "reviewer #{name} must be allowed" unless permissions[name] == "allow"
  end

  bash = permissions.fetch("bash")
  abort "reviewer bash must default to denied" unless bash["*"] == "deny"
  allowed = bash.select { |_, action| action == "allow" }.keys.sort
  expected = [
    "git diff --cached --name-only",
    "git diff --cached --name-status",
    "git diff --cached --patch",
    "git diff --cached --patch -- *",
    "git diff --cached --stat",
    "git show :*",
    "git show HEAD:*",
    "git status --short"
  ]
  abort "unexpected reviewer commands: #{allowed.join(", ")}" unless allowed == expected
' "$AGENT_FILE"

grep -q 'references/story-review.md' "$AGENT_FILE" ||
  fail "reviewer does not require the supplied shared protocol"
grep -q '"verdict": "pass|changes_requested|blocked"' "$REVIEW_FILE" ||
  fail "shared output schema is missing verdict"
grep -q '"learning_candidates"' "$REVIEW_FILE" ||
  fail "shared output schema is missing learning candidates"
grep -q 'retrieve only missing sections' "$REVIEW_FILE" ||
  fail "agent does not recover only missing evidence after truncation"

grep -q '`ralph-reviewer`' "$RALPH_FILE" ||
  fail "Ralph does not invoke the consolidated reviewer"
grep -q 'Required exact prepared branch: `branchName`' "$RALPH_FILE" ||
  fail "Ralph does not read the execution plan branch"
grep -q 'Set `passes: true` only provisionally' "$RALPH_FILE" ||
  fail "Ralph does not update execution plan completion"
grep -q '`memory.json`' "$RALPH_FILE" ||
  fail "Ralph does not define bounded review memory"
grep -q 'accepted_fixed' "$EXECUTION_FILE" ||
  fail "Ralph does not record finding dispositions"
grep -q 'task_id' "$RALPH_FILE" ||
  fail "Ralph does not resume the targeted review session"
grep -q 'Do not embed the' "$EXECUTION_FILE" ||
  fail "Ralph does not require compact reviewer Task prompts"
grep -q 'truncation alone is not blocking' "$EXECUTION_FILE" ||
  fail "Ralph still treats aggregate diff truncation as an immediate blocker"
grep -q 'do not read/create the missing file' "$EXECUTION_FILE" ||
  fail "Ralph may still produce a missing memory file tool error"

grep -q '^## Authorization and prepared branch' "$EXECUTION_FILE" ||
  fail 'Ralph is missing scoped standing authorization'
if grep -Ei 'auto.approval|ralph --auto|dev-browser' "$RALPH_FILE"; then
  fail 'Ralph still uses removed approval state or old browser skill'
fi
grep -q '`verify-interface`' "$EXECUTION_FILE" ||
  fail 'Ralph must use renamed browser verification skill'
grep -q 'including local/test operations, need explicit approval' "$EXECUTION_FILE" ||
  fail 'Docker and migrations must not receive standing authorization'

grep -q 'references/story-execution.md' "$RALPH_FILE" ||
  fail "Ralph does not load shared execution rules"
grep -q 'Never substitute `code-reviewer`' "$EXECUTION_FILE" ||
  fail "shared gate permits general-purpose reviewer substitution"

printf 'Ralph review contract validation passed.\n'
