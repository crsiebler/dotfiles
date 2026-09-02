#!/bin/bash

set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
RALPH_FILE="$ROOT_DIR/bin/ralph"
TEST_DIR=$(mktemp -d)
trap 'rm -rf "$TEST_DIR"' EXIT

mkdir -p "$TEST_DIR/bin" "$TEST_DIR/home/.config/opencode"
printf '{"userStories":[{"passes":false}]}\n' > "$TEST_DIR/prd.json"
printf 'test prompt\n' > "$TEST_DIR/home/.config/opencode/ralph.md"

cat > "$TEST_DIR/bin/opencode" <<'EOF'
#!/bin/bash
printf '%s\n' "$*" > "$RALPH_TEST_DIR/opencode.args"
EOF
chmod +x "$TEST_DIR/bin/opencode"

cat > "$TEST_DIR/bin/jq" <<'EOF'
#!/bin/bash
if [[ -f "$RALPH_TEST_DIR/opencode.args" ]]; then
  exit 0
fi
exit 1
EOF
chmod +x "$TEST_DIR/bin/jq"

run_ralph() {
  (
    cd "$TEST_DIR"
    HOME="$TEST_DIR/home" \
      PATH="$TEST_DIR/bin:$PATH" \
      RALPH_TEST_DIR="$TEST_DIR" \
      bash "$RALPH_FILE" "$@"
  )
}

run_ralph --model openai/gpt-5.4 --max-iterations 1 >/dev/null
grep -q -- '-m openai/gpt-5.4' "$TEST_DIR/opencode.args" || {
  printf 'FAIL: selected model was not passed to OpenCode\n' >&2
  exit 1
}

if run_ralph --model unsupported/model >/dev/null 2>&1; then
  printf 'FAIL: unsupported model was accepted\n' >&2
  exit 1
fi

printf 'Ralph model option validation passed.\n'
