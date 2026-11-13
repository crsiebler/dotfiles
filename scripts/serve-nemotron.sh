#!/usr/bin/env bash
# Optional foreground TensorFold server; never installs or downloads a model.
set -euo pipefail

revision=d9d758fb83953437f7263256b0d96157e2a348b8
repo=TensorFold/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-MLX-4bit
cache_root="${HF_HUB_CACHE:-${HF_HOME:-$HOME/.cache/huggingface}/hub}"
model="$cache_root/models--${repo//\//--}/snapshots/$revision"

if ! command -v tensorfold >/dev/null 2>&1; then
  printf 'TensorFold is required; see docs/local-nemotron.md.\n' >&2
  exit 1
fi
if [[ ! -f "$model/model.safetensors.index.json" ||
      ! -f "$model/mtp-4bit.safetensors" ]]; then
  printf 'Download the pinned checkpoint first:\n  tensorfold pull %s@%s\n' \
    "$repo" "$revision" >&2
  exit 1
fi

exec tensorfold serve "$model" \
  --name nemotron-lightning \
  --host 127.0.0.1 --port 8082 \
  --context 65536 --max-tokens 8192 \
  --parallel 1 --prompt-cache-gib 0.5 \
  --no-thinking --no-update-check
