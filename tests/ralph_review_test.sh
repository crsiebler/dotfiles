#!/bin/bash

set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
AGENT_FILE="$ROOT_DIR/ai/opencode/agents/ralph-reviewer.md"
RALPH_FILE="$ROOT_DIR/ai/opencode/agents/ralph.md"

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

[[ -f "$AGENT_FILE" ]] || fail "missing ralph-reviewer agent"
[[ -f "$RALPH_FILE" ]] || fail "missing Ralph primary agent"

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

grep -q '"verdict": "pass|changes_requested|blocked"' "$AGENT_FILE" ||
  fail "agent output schema is missing verdict"
grep -q '"learning_candidates"' "$AGENT_FILE" ||
  fail "agent output schema is missing learning candidates"
grep -q 'do not block immediately' "$AGENT_FILE" ||
  fail "agent does not recover from aggregate diff truncation"

grep -q '`ralph-reviewer`' "$RALPH_FILE" ||
  fail "Ralph does not invoke the consolidated reviewer"
grep -q '`memory.json`' "$RALPH_FILE" ||
  fail "Ralph does not define bounded review memory"
grep -q 'accepted_fixed' "$RALPH_FILE" ||
  fail "Ralph does not record finding dispositions"
grep -q 'task_id' "$RALPH_FILE" ||
  fail "Ralph does not resume the targeted review session"
grep -q 'Do not embed the staged patch' "$RALPH_FILE" ||
  fail "Ralph does not require compact reviewer Task prompts"
grep -q 'Aggregate patch truncation is not itself a blocker' "$RALPH_FILE" ||
  fail "Ralph still treats aggregate diff truncation as an immediate blocker"
grep -q 'Do not call Read when `memory.json` is absent' "$RALPH_FILE" ||
  fail "Ralph may still produce a missing memory file tool error"

if grep -A220 '^## Mode-Aware Review Stabilization Loop' "$RALPH_FILE" |
  grep -Eq '`(code-reviewer|qa-expert|ui-designer|ux-researcher|security-engineer)`'; then
  fail "Ralph local review loop still delegates to general-purpose specialists"
fi

printf 'Ralph review contract validation passed.\n'
