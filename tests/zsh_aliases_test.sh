#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
actual="$(
  REPO_ROOT="$repo_root" zsh -f -c '
    alias dcr="docker compose run"
    source "$REPO_ROOT/aliases/.docker_aliases"
    whence -w dcr
    print -r -- "${aliases[dcr]}"
  '
)"
expected=$'dcr: alias\ndocker compose run'

if [[ "$actual" != "$expected" ]]; then
  printf 'Expected:\n%s\nActual:\n%s\n' "$expected" "$actual" >&2
  exit 1
fi

printf 'Zsh alias regression tests passed.\n'
