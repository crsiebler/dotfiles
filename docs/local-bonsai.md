# Ternary Bonsai 2 27B on macOS with OpenCode

Research checked September 17, 2026 using Exa and Context7. This guide targets
an M5 Max with 36GB unified memory. It documents installation and configuration;
the repository's OpenCode source now includes a selectable `bonsai` provider.
No runtime, weights, or user-level configuration have been installed.

**Recommendation:** evaluate PrismML's **GGUF PQ2_0** with its llama.cpp fork,
one server slot, and **65,536 context tokens**. With small PostgreSQL containers,
VSCode, and a few Chrome tabs open, **131,072 tokens is a reasonable next target**
after measuring memory pressure. This is an initial integration recommendation,
not evidence that llama.cpp is faster than MLX. Context sizes are estimates, not
local benchmark results.

## Model and runtime selection

[PrismML announced Bonsai 2 on September 17](https://prismml.com/news/bonsai-2-27b).
It is derived from Qwen3.8-27B and released under Apache 2.0.

| Package | Published file size | Required runtime |
| --- | --- | --- |
| GGUF PTQ1_0 | 5.95GB language weights | PrismML llama.cpp fork |
| GGUF PQ2_0 | 7.21GB language weights | PrismML llama.cpp fork; published Apple measurement path |
| MLX 2-bit | 8.60GB including 0.92GB vision tower | Model's bundled custom loader |

The [GGUF card](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf)
and [MLX card](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-mlx-2bit)
distinguish these formats. The 5.9GB headline is not total runtime memory, nor
the size of the MLX package. PQ2_0 is the practical first choice here because
36GB leaves room for its larger packing and it is the measured Apple path.

Do not use stock llama.cpp, Ollama, or the existing `mlx_lm.server` command as
an assumed drop-in runtime. The GGUF formats require custom kernels and Hadamard
activation transforms. The MLX artifact declares `prism_hadamard_qwen35` and needs
its bundled loader; ordinary loaders may produce incorrect output.

PrismML's 98.2% retention is a vendor aggregate, not identical task success.
The announcement reports 83.9 versus 85.4; the model card uses a different
14-benchmark aggregate of 84.78 versus 86.32. The card qualifies its approximately
47 tok/s M5 Max result as an earlier pre-rotation build pending remeasurement.
Neither claim was independently reproduced here. See the sources above.

## MLX versus llama.cpp: speed remains unverified

An Exa search found no direct, same-model, same-hardware comparison of Bonsai 2's
custom MLX loader against PrismML llama.cpp on M5 Max. MLX may be faster, but the
available evidence does not establish a winner. The approximately 47 tok/s figure
on the MLX model card was measured with **llama.cpp Metal**, not MLX, and carries
the earlier-build qualification above.

For text-only weights, the published sizes are 7.67GB for MLX and 7.21GB for
PQ2_0. The smaller GGUF representation could reduce memory traffic, but kernel
efficiency can outweigh that difference; file size alone does not predict speed.
The MLX package's 8.60GB total includes vision weights. These details come from
the [MLX card](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-mlx-2bit).

The [pack runtime notes](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-mlx-2bit/raw/main/PACK-RUNTIME.md)
still describe a text-only preview while the model card describes a vision loader.
Reconcile that documentation mismatch against the exact downloaded revision
before adopting MLX. Neither an ordinary MLX loader nor generic Qwen benchmarks
establish Bonsai 2 correctness or performance.

Keep llama.cpp as the documented first integration, then compare MLX with the
same model revision, prompts, sampling, context, output length, and app workload.
Measure cold and cached prompt processing, time to first answer token, generation
speed, peak memory/swap, and total time for a complete OpenCode tool-call cycle.
Separate reasoning tokens from answer tokens and verify equivalent useful output.
Choose based on that workload; no local comparison has yet been performed.

## Is an Ollama Modelfile needed?

**No.** A [Modelfile](https://docs.ollama.com/modelfile) configures a model inside
Ollama; it is not a general Hugging Face model configuration. It cannot supply
the custom Bonsai kernels and transforms missing from an unsupported runtime.
The documented setup consists of a downloaded GGUF artifact, PrismML's
`llama-server` launch arguments, and an OpenCode provider pointing to its API.
The GGUF contains model metadata and the chat template; `--jinja` enables its
tool-aware formatting. Preserve that template rather than inventing a replacement.
No Modelfile is created. A separate launcher could later make the documented
server command convenient without introducing Ollama.

## Context budget with development apps open

Budget in **GiB** below (1 GiB = 1,073,741,824 bytes), treating the requested
36GB Mac as approximately 36GiB physical memory; verify with `sysctl -n hw.memsize`.
The 7.21 decimal-GB PQ2_0 file is approximately **6.72GiB**.

Planning assumptions, not measured application usage:

| Allocation | Working estimate |
| --- | --- |
| macOS and background services | 5–7GiB |
| Docker VM, PostgreSQL, and small companion containers combined | 2–4GiB |
| VSCode, extensions, and language servers | 1–2GiB |
| Chrome with a few ordinary tabs | 1–2GiB |
| OpenCode and terminal | 0.5–1GiB |
| PQ2_0 language weights | About 6.72GiB |
| Inference buffers, recurrent state, allocator overhead | Allow 2–4GiB |
| Spare capacity for workload spikes | Reserve 3GiB |

Docker's configured VM ceiling is not necessarily current usage. Count the VM
and its containers together rather than adding the same memory twice. Heavy
queries, large `shared_buffers`, indexing, browser web apps, or multiple language
servers can exceed these assumptions. Do not run the older MLX model alongside
Bonsai when evaluating this budget.

The model's [architecture configuration](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-mlx-2bit/raw/main/config.json)
has 16 full-attention layers, 4 KV heads, and head dimension 256. With FP16 K/V,
the approximate growing cache is:

```text
16 layers × 4 KV heads × 256 dimensions × 2 (K and V) × 2 bytes
= 65,536 bytes/token = 64 KiB/token
```

This agrees with [PrismML's context-sizing helper](https://github.com/PrismML-Eng/Bonsai-demo/blob/main/scripts/common.sh).
Linear-attention state and other allocations remain additional. The helper
selects 65,536 tokens for its 36–71GiB tier. Exact server allocations, cache
snapshots, and processing peaks must still be checked from logs and measurements.

| Total context | Approx. FP16 KV | Weights + KV only | Recommendation with apps open |
| --- | --- | --- | --- |
| 32,768 | 2GiB | 8.72GiB | Fallback for heavier workloads |
| 65,536 | 4GiB | 10.72GiB | Conservative daily default |
| 131,072 | 8GiB | 14.72GiB | Plausible target after a load test |
| 196,608 | 12GiB | 18.72GiB | Light-workload experiment; little margin at upper app estimates |
| 262,144 | 16GiB | 22.72GiB | Avoid as the default with this app mix |

For example, 12GiB for OS/apps + 6.72GiB weights + 3GiB runtime overhead +
8GiB KV + 3GiB spare = **32.72GiB** at 128K. At the upper app/overhead estimates,
128K can exceed the budget; 64K leaves more margin. A full 256K context would
need about **40.72GiB** using the same central assumptions and spare capacity.
Quantized KV might reduce this, but is outside this baseline and needs separate
quality and runtime verification.

Context includes instructions, MCP schemas, files, conversation, tool results,
reasoning, and the final answer. With 8,192 output tokens reserved, 64K leaves at
most 57,344 input tokens and 128K leaves 122,880, before OpenCode's own compaction
margin. These are not all available for source files. Long prompts also increase
prefill latency; fitting in memory does not establish interactive performance.

## Install the compatible runtime and model

The commands below are for a future manual installation. Use a new dedicated
directory, not this dotfiles checkout. Required tools: native arm64 macOS, Xcode
Command Line Tools, Git, CMake, and `curl`. Arrange missing prerequisites
separately. Allow roughly 15–20GB free disk space for weights and the build.

Build from the PrismML fork so this path does not require a binary-download
helper that changes quarantine attributes. The inspected demo currently pins
`prism-b9596-9fcaed7`; check its [download script](https://github.com/PrismML-Eng/Bonsai-demo/blob/main/scripts/download_binaries.sh)
and [release notes](https://github.com/PrismML-Eng/llama.cpp/releases) again at
installation time because this release is new. Do not substitute stock upstream.

```sh
mkdir -p "$HOME/Models/bonsai-2"
cd "$HOME/Models/bonsai-2"
git clone --branch prism-b9596-9fcaed7 --depth 1 \
  https://github.com/PrismML-Eng/llama.cpp.git runtime
cmake -S runtime -B runtime/build \
  -DCMAKE_BUILD_TYPE=Release -DGGML_METAL=ON
cmake --build runtime/build --config Release -j 4 --target llama-server
./runtime/build/bin/llama-server --version
git -C runtime rev-parse HEAD
mkdir -p models
curl --fail --location --retry 3 \
  'https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/resolve/main/Ternary-Bonsai-2-27B-PQ2_0.gguf' \
  --output models/Ternary-Bonsai-2-27B-PQ2_0.gguf
shasum -a 256 models/Ternary-Bonsai-2-27B-PQ2_0.gguf
```

Record the resolved runtime commit and compare the downloaded model's SHA-256
with the file's hash on Hugging Face. Pin that model repository revision for
repeatable later downloads instead of relying permanently on `main`. Source
build steps are adapted from the official GGUF card; they have not been executed
here. If the pinned release cannot load this artifact, reconcile the current
model/runtime requirements before proceeding, rather than ignoring loader errors.

## Serve a local OpenAI-compatible API

Run in the dedicated installation directory in a foreground terminal:

```sh
./runtime/build/bin/llama-server \
  -m ./models/Ternary-Bonsai-2-27B-PQ2_0.gguf \
  --alias bonsai-2-27b \
  --host 127.0.0.1 --port 8081 \
  -ngl 99 -fa on -c 65536 -np 1 \
  --cache-type-k f16 --cache-type-v f16 \
  --jinja --reasoning-format deepseek \
  --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0
```

Port 8081 keeps this separate from the existing MLX provider at 8080. Check for
an existing listener before starting; do not automatically terminate it. `-np 1`
uses one slot so parallel requests do not multiply the working memory budget.
`-c` bounds total context; avoid automatic/full-model context for the first run.
No vision projector or speculative draft model is loaded in this baseline.

The [fork server API](https://github.com/PrismML-Eng/llama.cpp/blob/prism/tools/server/README.md)
documents these flags. `--jinja` enables native tool calls;
`--reasoning-format deepseek` puts thinking into `reasoning_content`. Sampling
matches the model card's thinking guidance. Thinking stays enabled; the card
supports default `xhigh` and `medium`, and explicitly does not support `low`.
Reasoning-effort variants are omitted until the client round trip is verified.

## Configure OpenCode using an opt-in profile

The checked-in [OpenCode source](../ai/opencode/opencode.json) now includes the
`bonsai` provider shown below, retaining the existing MLX provider and global
model selection. OpenCode connects to the server; adding the provider does not
download or load the Hugging Face model. Start the compatible server first.
After separately authorized `make install-opencode`, restart OpenCode and select
`bonsai/bonsai-2-27b` with `/models` or `opencode --model bonsai/bonsai-2-27b`.
The installer copies configuration; it does not provision the inference runtime.

Save the following example as `opencode-bonsai.json` in the dedicated installation
directory if you also want a profile selecting Bonsai for build and plan. This
full profile remains a documentation example; only its provider section was added
to the repository source. It follows the current documented OpenCode
configuration format used by this repository, as verified through Context7's
`/websites/opencode_ai` [provider documentation](https://opencode.ai/docs/providers/).

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "bonsai/bonsai-2-27b",
  "agent": {
    "build": { "model": "bonsai/bonsai-2-27b" },
    "plan": { "model": "bonsai/bonsai-2-27b" }
  },
  "provider": {
    "bonsai": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "PrismML Bonsai Local",
      "options": {
        "baseURL": "http://127.0.0.1:8081/v1",
        "apiKey": "none",
        "timeout": false
      },
      "models": {
        "bonsai-2-27b": {
          "name": "Ternary Bonsai 2 27B PQ2_0",
          "limit": { "context": 65536, "output": 8192 },
          "modalities": { "input": ["text"], "output": ["text"] },
          "tool_call": true,
          "reasoning": true,
          "interleaved": { "field": "reasoning_content" },
          "temperature": true
        }
      }
    }
  }
}
```

The model key matches `--alias`; `interleaved` preserves returned reasoning in
later messages. These are capability declarations, not proof of working tools.
`apiKey: none` is a placeholder for this loopback development server, not an
authentication mechanism. Do not expose it to a network without a separate
authenticated deployment design. `timeout: false` allows slow local prefill;
an unresponsive request must be cancelled manually.

From the project you want to work on:

```sh
OPENCODE_CONFIG="$HOME/Models/bonsai-2/opencode-bonsai.json" \
  opencode --model bonsai/bonsai-2-27b
```

[OpenCode merges configurations](https://opencode.ai/docs/config/); this is not an
isolated profile. Global settings still apply and project settings may override
the custom file. Your repository's `astra.json` pins the build agent to Astra;
do not use that overlay for this trial. The example selects build and plan
explicitly, but other custom agents can retain pinned cloud models. Confirm the
active model before work. Keep existing MCP permission policy; enabling many
tools adds prompt tokens and prefill time. No global installation target is
needed to try this custom profile.

## Verify before relying on agent work

Check readiness and that the served model is named `bonsai-2-27b`:

```sh
curl --fail-with-body http://127.0.0.1:8081/health
curl --fail-with-body http://127.0.0.1:8081/v1/models
curl --fail-with-body http://127.0.0.1:8081/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"bonsai-2-27b","messages":[{"role":"user","content":"Reply with READY."}],"max_tokens":8192,"stream":false}'
```

Follow [PrismML's tool-call example](https://github.com/PrismML-Eng/Bonsai-demo/blob/main/TOOLS.md)
against port 8081 with `model: bonsai-2-27b`. Require structured
`choices[0].message.tool_calls`, then append the assistant message and a tool
result with the matching `tool_call_id`; verify a final answer. Repeat streaming
and check tool-call deltas and separate reasoning. The model proposes a call;
the client executes it. Literal tool markup in answer text is not success.
Finally, use a disposable OpenCode project for a harmless file-read task and
confirm it completes the tool-result cycle with this local model.

For memory validation, keep the specified apps and containers running. Check
Activity Monitor's Memory Pressure and Swap Used before and during a realistic
long-prompt run. Server startup alone does not test peak prefill usage. Inspect
logs for actual cache/buffer allocations, and use `docker stats --no-stream`
for container context while counting the Docker VM in macOS memory totals.
Sustained yellow/red pressure or growing swap under load means reduce context.

If 64K stays comfortable, restart the foreground server yourself with
`-c 131072` and change the profile's `limit.context` to `131072` together.
Keep the output reserve at 8192 initially. Test a genuinely long conversation,
not just a short greeting; fall back to 64K or 32K if needed. Metal working-set
limits can also constrain allocation, so free system RAM alone is not proof of
fit. Do not raise kernel memory limits to force a larger context.

## Verification status

Sources, command flags, model identifiers, configuration structure, and memory
arithmetic were reviewed. No model download, runtime build, configuration
installation, API call, hardware measurement, or end-to-end OpenCode test was
performed while writing this guide. Reported performance remains vendor evidence.
The provider source and documentation example are checked for matching content;
local source validation does not establish runtime or tool-call compatibility.
