# Bonsai 2 MLX for OpenCode

Source configuration updated September 27, 2026 for an M5 Max with 36GB RAM.
This replaces the former PQ2_0 llama.cpp and Qwen3-Coder provider configurations.
The uv-tool runtime is installed and its server help command was verified.
The user reports downloading the weights. Live model verification is pending.

## Files and defaults

- `ai/opencode/opencode.json`: the sole local coding provider, `bonsai`, using
  `http://127.0.0.1:8081/v1` and model ID
  `prism-ml/Ternary-Bonsai-2-27B-mlx-2bit`.
- `aliases/.aliases`: `mlx-bonsai` foreground server function, no installation logic.

The provider declares text input, tool calls, and separate `reasoning_content`.
These declarations require a real streaming/tool-result round-trip test before
relying on agent work. Vision is deliberately not advertised in this coding
profile even though the model includes vision weights.

Initial total context is 65,536 tokens; output allowance is 8,192. The server
requests the same cache budget, one concurrent sequence, 512-token prefill
chunks, and a default thinking budget of 4,096 tokens within the output allowance.
The thinking budget is a length cap, not the model's `medium` reasoning effort.
Requests can override server generation defaults. A cache budget is not proof
of a hard HTTP input-length guard or reliable recall at that length.

64K is a starting point, not a measured limit. After testing with the editor,
browser and containers open, 128K is a candidate: change the launcher cache
budget and provider context together. Keep the output reserve. Context includes
instructions, tools, files, tool results, reasoning, and answers. At 64K with an
8K output reserve, at most 57,344 input tokens remain before compaction margins.
Do not raise macOS memory limits or enable cache quantization to force a fit.

## Provision separately

Use native arm64 Python 3.11 through an isolated uv tool. The following commands
are a manual setup recipe, not something the dotfiles installer executes.
No Conda environment or checkout-relative launcher is required:

```sh
uv tool install --python 3.11 --with "mlx==0.32.2" \
  --with "transformers==5.14.1" "mlx-vlm==0.7.2"
hf download prism-ml/Ternary-Bonsai-2-27B-mlx-2bit \
  --local-dir "$HOME/Models/bonsai-2-mlx"
```

The pinned packages are `mlx==0.32.2`, `mlx-vlm==0.7.2`, and
`transformers==5.14.1`; transitive dependencies are not locked. Record the resolved
versions and downloaded Hugging Face snapshot revision when provisioning.
The model is approximately 8.60GB on disk; allow additional room for dependencies
and caches. Download the complete model with the separately available `hf` CLI before
launching; the function loads that local directory. Public weights do not
require a login.

No fork build, macOS patch, global Python update, or audio-environment change is
required for this stock-package route. The released native loader performs the
signed Hadamard activation transforms and inverse embedding transform itself.
Do not rename the architecture to ordinary Qwen or substitute a generic loader.
Avoid the broad demo `setup.sh`: it provisions additional runtimes and optional
applications beyond this configuration.

## Start and select

Check that port 8081 is free; do not terminate an existing listener automatically.
After the updated aliases are installed, open a new shell and run:

```sh
mlx-bonsai
```

This replaces `mlx-qwen` and invokes `mlx_vlm.server` directly. The only model
path is `$HOME/Models/bonsai-2-mlx`, independent of where the repository is cloned.
Extra arguments are forwarded to the server. The function binds to loopback and
stays in the foreground; stop it with Ctrl-C when finished, especially before
loading audio. It starts the model server, not OpenCode.

When reloading aliases in an existing shell, first remove its old definitions:

```sh
unalias mlx-bonsai 2>/dev/null
unfunction mlx-qwen 2>/dev/null
source "$HOME/.aliases"
```

The local-path server may advertise a different model ID than the original
Hugging Face identifier in the provider. Inspect `/v1/models` and match the
OpenCode provider model ID before using the client; this remains unverified.

The provider must also exist in installed OpenCode settings. Repository edits
do not activate it automatically. A separately authorized installation can copy
it, but full `make install` is unnecessary and changes unrelated shell settings.
Preserve other providers and permission rules during a scoped installed update.

After provider activation, from the coding project:

```sh
opencode --model bonsai/prism-ml/Ternary-Bonsai-2-27B-mlx-2bit
```

Alternatively, choose Bonsai through `/models`. No separate local profile is
needed. The base configuration preserves cloud defaults for explicitly pinned
agents and the small model; selecting Bonsai does not make every auxiliary task
local. Confirm the active model and avoid the Astra overlay for local work.

The model card recommends temperature 1.0, top-p 0.95, top-k 20, and min-p 0 for
thinking mode. Exact sampling forwarding through OpenCode remains unverified;
removing the selection overlay also removes its agent-level sampling overrides.

## Verification before daily use

1. Confirm installed package versions match the pinned requirements.
2. Start the server and inspect `/v1/models`; verify the expected model ID.
3. Submit a short chat request, then test streamed reasoning and a structured
   tool call followed by its matching tool result and a final answer.
4. Run a harmless OpenCode file-read task. Text containing tool markup alone is
   not proof of a successful structured tool call.
5. Test a realistic long conversation with normal apps open. Record peak memory,
   swap growth, prompt-processing latency, and completed task quality before
   increasing context. Short-prompt tokens/sec do not predict long-context speed.

## Removing obsolete local coding models

1. Inspect the inventory and exact model directories; preserve audio weights.
2. Stop any process using a selected model before deleting it yourself.
3. Remove only the selected model directory or use its cache manager. Hugging
   Face snapshot symlinks and blobs are one cache entry, not independent copies.
4. Keep rollback configuration copies until the new provider is verified.
   Never remove an entire shared cache or runtime environment just because it
   contains one old coding model. No automatic model deletion is included.

## Evidence and limitations

- [PrismML pinned requirements](https://github.com/PrismML-Eng/Bonsai-demo/blob/main/scripts/requirements-mlx-vlm.txt)
- [PrismML server selection](https://github.com/PrismML-Eng/Bonsai-demo/blob/main/scripts/start_mlx_server.sh)
- [Released native loader](https://github.com/Blaizzy/mlx-vlm/blob/v0.7.2/mlx_vlm/models/prism_hadamard_qwen35/prism_hadamard_qwen35.py)
- [Released server flags](https://github.com/Blaizzy/mlx-vlm/blob/v0.7.2/mlx_vlm/server/cli.py)
- [Model card](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-mlx-2bit)

Source inspection confirms the loader, dependency pins, and launcher flags.
Static configuration checks do not prove live loading, tool calls, sampling
forwarding, or long-context fit. There is no standalone repository typecheck.
