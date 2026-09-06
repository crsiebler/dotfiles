#!/bin/bash

set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
RALPH_FILE="$ROOT_DIR/bin/ralph"
TEST_DIR=$(mktemp -d "$ROOT_DIR/tests/ralph_model.XXXXXX")
trap 'rm -rf "$TEST_DIR"' EXIT

mkdir -p "$TEST_DIR/bin" "$TEST_DIR/home/.config/opencode/agents" "$TEST_DIR/no-cli"
# Keep fixture Git commands independent of user signing, hooks, and includes.
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_COMMON_DIR
unset XDG_CONFIG_HOME
command -v jq >/dev/null || { printf 'real jq required\n' >&2; exit 1; }
ln -s "$(command -v jq)" "$TEST_DIR/no-cli/jq"
git -C "$TEST_DIR" init -q
git -C "$TEST_DIR" symbolic-ref HEAD refs/heads/ralph/test
git -C "$TEST_DIR" -c user.name=Test -c user.email=test@example.invalid \
  -c commit.gpgsign=false commit --allow-empty -qm fixture
write_plan() {
  printf '%s\n' '{"branchName":"ralph/test","userStories":[{"id":"US-001","title":"Test","description":"Test story","acceptanceCriteria":["Typecheck passes"],"priority":1,"passes":false}]}' > "$TEST_DIR/plan.json"
}
write_plan
printf '%s\n' '---' 'description: test Ralph agent' 'mode: primary' '---' 'test prompt' > "$TEST_DIR/home/.config/opencode/agents/ralph.md"

cat > "$TEST_DIR/bin/opencode" <<'EOF'
#!/bin/bash
printf '%s\n' "$@" >> "$RALPH_TEST_DIR/opencode.args"
case "${RALPH_TEST_ACTION:-complete}" in
  complete)
    jq '.userStories[].passes = true' plan.json > plan.next
    mv plan.next plan.json
    ;;
  branch|branchcomplete)
    git symbolic-ref HEAD refs/heads/ralph/changed
    if [[ "$RALPH_TEST_ACTION" == branchcomplete ]]; then
      jq '.userStories[].passes = true' plan.json > plan.next
      mv plan.next plan.json
    fi
    ;;
  invalid) printf '{}\n' > plan.json ;;
  fail) exit 23 ;;
  unchanged) : ;;
esac
EOF
chmod +x "$TEST_DIR/bin/opencode"

cat > "$TEST_DIR/bin/codex" <<'EOF'
#!/bin/bash
printf 'unexpected Codex invocation\n' > "$RALPH_TEST_DIR/codex.called"
exit 99
EOF
chmod +x "$TEST_DIR/bin/codex"

run_ralph() {
  (
    cd "$TEST_DIR"
    rm -f "$TEST_DIR/opencode.args"
    HOME="$TEST_DIR/home" \
      PATH="${RALPH_TEST_PATH:-$TEST_DIR/bin:$PATH}" \
      RALPH_TEST_DIR="$TEST_DIR" \
      /bin/bash "$RALPH_FILE" "$@"
  )
}

fail() { printf 'FAIL: %s\n' "$1" >&2; exit 1; }
reject() {
  local expected=$1
  shift
  if run_ralph "$@" > "$TEST_DIR/output" 2>&1; then
    fail "accepted $*"
  fi
  grep -q -- "$expected" "$TEST_DIR/output" || fail "missing error: $expected"
  [[ ! -e "$TEST_DIR/opencode.args" ]] || fail 'invoked OpenCode on invalid input'
  [[ ! -e "$TEST_DIR/codex.called" ]] || fail 'invoked unsupported Codex runner'
}

reject '--auto has been removed' --auto
reject '--auto has been removed' --auto=true
for option in --model --mode --max-iterations; do
  reject 'requires a value' "$option"
  reject 'requires a value' "$option" --help
  reject 'requires a value' "$option" ''
done
reject 'unknown option' --harness
for harness in opencode codex other; do
  reject 'unknown option' --harness "$harness"
  reject 'unknown option' "--harness=$harness"
done
reject 'mode must be' --mode other
for count in 0 -1 1.5 abc 999999999999999999999999999; do
  reject 'positive integer' --max-iterations "$count"
done
reject 'unsupported model' --model unsupported/model
reject 'model identifier' --model 'native model'
reject 'model identifier' --model $'native\nmodel'
reject 'unsupported model' --model native/provider/model
reject 'unknown option' --bypass-review

# A same-name tag must not change the identity of the prepared branch.
git -C "$TEST_DIR" update-ref refs/tags/ralph/test HEAD
run_ralph --model openai/gpt-5.4 --max-iterations 1 >/dev/null
{
  for expected in run --agent ralph -m openai/gpt-5.4 --variant high; do
    IFS= read -r actual
    [[ "$actual" == "$expected" ]] || fail "incorrect argv: expected $expected"
  done
} < "$TEST_DIR/opencode.args"
for expected in 'ralph' 'openai/gpt-5.4' 'high' 'Harness: opencode' \
  'Execution mode: standard' 'Maximum iterations: 1' 'Iteration: 1 of 1' \
  'Model: openai/gpt-5.4' 'Model source: explicit'; do
  grep -qx -- "\(- \)\{0,1\}$expected" "$TEST_DIR/opencode.args" || fail "missing argument/context: $expected"
done
if grep -Ei -- 'auto.approval|--auto|bypass|full-auto|dangerously' "$TEST_DIR/opencode.args"; then
  fail 'approval bypass in harness arguments/runtime'
fi
write_plan
run_ralph --max-iterations 1 >/dev/null
grep -q 'Model: openai/gpt-5.6-sol-fast' "$TEST_DIR/opencode.args" || fail 'default model changed'
grep -q 'Model source: default' "$TEST_DIR/opencode.args" || fail 'default source missing'
for mode in fast deep; do
  write_plan
  run_ralph --mode "$mode" --max-iterations 1 >/dev/null
  grep -qx -- "- Execution mode: $mode" "$TEST_DIR/opencode.args" || fail 'mode context lost'
done

# Codex Spark is an OpenCode model, not a runner selection.
write_plan
run_ralph --model openai/gpt-5.3-codex-spark --max-iterations 1 >/dev/null
grep -qx -- '- Model: openai/gpt-5.3-codex-spark' "$TEST_DIR/opencode.args" || fail 'Spark model lost'
grep -qx -- '- Model source: explicit' "$TEST_DIR/opencode.args" || fail 'explicit source lost'

# Valid completion needs neither an OpenCode binary/agent nor Git.
RALPH_TEST_PATH="$TEST_DIR/no-cli" run_ralph > "$TEST_DIR/output"
grep -q 'All user stories completed' "$TEST_DIR/output" || fail 'completion short circuit'
RALPH_TEST_PATH="$TEST_DIR/no-cli" run_ralph --help >/dev/null

# Dependency diagnostics and option parsing must not depend on harness installs.
mv "$TEST_DIR/plan.json" "$TEST_DIR/plan.saved"
reject 'plan.json not found'
reject 'unknown option' --unknown
# A complete legacy artifact must not substitute for the execution plan.
mv "$TEST_DIR/plan.saved" "$TEST_DIR/prd.json"
reject 'plan.json not found'
mv "$TEST_DIR/prd.json" "$TEST_DIR/plan.json"
write_plan
mkdir -p "$TEST_DIR/empty-bin" "$TEST_DIR/git-only"
RALPH_TEST_PATH="$TEST_DIR/empty-bin" reject 'jq command not found'
for dependency in jq git grep; do
  ln -s "$(command -v "$dependency")" "$TEST_DIR/git-only/$dependency"
done
RALPH_TEST_PATH="$TEST_DIR/git-only" reject 'opencode command not found'
mv "$TEST_DIR/home/.config/opencode/agents/ralph.md" "$TEST_DIR/agent.saved"
reject 'ralph.md not found'
mv "$TEST_DIR/agent.saved" "$TEST_DIR/home/.config/opencode/agents/ralph.md"

# Custom XDG installation: no agent file exists under the default HOME root.
mkdir -p "$TEST_DIR/custom config/opencode/agents"
mv "$TEST_DIR/home/.config/opencode/agents/ralph.md" \
  "$TEST_DIR/custom config/opencode/agents/ralph.md"
XDG_CONFIG_HOME="$TEST_DIR/custom config" run_ralph --max-iterations 1 > "$TEST_DIR/output"
grep -Fq "Ralph agent file found: $TEST_DIR/custom config/opencode/agents/ralph.md" \
  "$TEST_DIR/output" || fail 'custom XDG agent preflight path missing'
if grep -Eq 'Using Ralph agent from|Loaded Ralph agent' "$TEST_DIR/output"; then
  fail 'file existence must not claim which agent OpenCode loaded'
fi
mv "$TEST_DIR/custom config/opencode/agents/ralph.md" \
  "$TEST_DIR/home/.config/opencode/agents/ralph.md"
write_plan
XDG_CONFIG_HOME="$TEST_DIR/custom config" reject 'ralph.md not found'
XDG_CONFIG_HOME='relative/config' reject 'XDG_CONFIG_HOME must be an absolute path'
XDG_CONFIG_HOME='' run_ralph --max-iterations 1 > "$TEST_DIR/output"
grep -Fq "Ralph agent file found: $TEST_DIR/home/.config/opencode/agents/ralph.md" \
  "$TEST_DIR/output" || fail 'empty XDG override must use HOME fallback'

# Validate actual JSON rather than replacing jq with a completion stub.
for expression in 'del(.branchName)' '.branchName = ""' '.userStories = []' \
  '.userStories = [null]' '.userStories = [true]' '.userStories = {}' \
  'del(.userStories[0].id)' '.userStories[0].title = " "' \
  'del(.userStories[0].description)' '.userStories[0].acceptanceCriteria = []' \
  '.userStories[0].acceptanceCriteria = [1]' '.userStories[0].priority = "1"' \
  '.userStories[0].priority = -1' '.userStories[0].priority = 1.5' \
  '.userStories[0].passes = "true"' 'del(.userStories[0].passes)' \
  '.userStories += .userStories'; do
  write_plan
  jq "$expression" "$TEST_DIR/plan.json" > "$TEST_DIR/plan.next"
  mv "$TEST_DIR/plan.next" "$TEST_DIR/plan.json"
  reject 'invalid plan.json'
done
printf '{\n' > "$TEST_DIR/plan.json"
reject 'invalid plan.json'
write_plan
printf '{}\n' >> "$TEST_DIR/plan.json"
reject 'invalid plan.json'

write_plan
for branch in $'ralph/test\n' $'ralph/test\n\n'; do
  jq --arg branch "$branch" '.branchName = $branch' "$TEST_DIR/plan.json" > "$TEST_DIR/plan.next"
  mv "$TEST_DIR/plan.next" "$TEST_DIR/plan.json"
  reject 'branch mismatch'
done
write_plan
git -C "$TEST_DIR" symbolic-ref HEAD refs/heads/ralph/wrong
reject 'branch mismatch'
for branch in main master; do
  git -C "$TEST_DIR" symbolic-ref HEAD "refs/heads/$branch"
  jq --arg branch "$branch" '.branchName = $branch' "$TEST_DIR/plan.json" > "$TEST_DIR/plan.next"
  mv "$TEST_DIR/plan.next" "$TEST_DIR/plan.json"
  reject 'protected branch'
done
git -C "$TEST_DIR" symbolic-ref HEAD refs/heads/ralph/test
git -C "$TEST_DIR" checkout --detach -q
reject 'detached HEAD'
git -C "$TEST_DIR" symbolic-ref HEAD refs/heads/ralph/test

for action in branch branchcomplete invalid unchanged fail; do
  write_plan
  git -C "$TEST_DIR" symbolic-ref HEAD refs/heads/ralph/test
  result=0
  RALPH_TEST_ACTION="$action" run_ralph --max-iterations 2 > "$TEST_DIR/output" 2>&1 || result=$?
  if [[ "$result" == 0 ]]; then
    fail "unexpected success: $action"
  fi
  if [[ "$action" == fail ]]; then
    [[ "$result" == 23 ]] || fail 'harness exit status was not preserved'
  fi
  count=$(grep -cx 'run' "$TEST_DIR/opencode.args")
  if [[ "$action" == unchanged ]]; then
    [[ "$count" == 2 ]] || fail 'iteration limit not enforced'
    grep -q 'Reached maximum iterations (2)' "$TEST_DIR/output" || fail 'missing limit error'
  else
    [[ "$count" == 1 ]] || fail "unsafe next iteration: $action"
    case "$action" in
      branch|branchcomplete) expected='branch mismatch' ;;
      invalid) expected='invalid plan.json' ;;
      fail) expected='OpenCode failed (exit 23)' ;;
    esac
    grep -Fq "$expected" "$TEST_DIR/output" || fail "missing diagnostic: $action"
  fi
done

printf 'Ralph harness, model, plan, branch and iteration validation passed.\n'
