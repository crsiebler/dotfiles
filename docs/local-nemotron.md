# Optional TensorFold Nemotron provider

Pilot performed November 12, 2026 on Apple M5 Max, 36 GiB unified memory,
OpenCode v2.1.4. This adds `tensorfold/nemotron-lightning`; Bonsai's provider,
launcher, weights and runtime remain unchanged. The default session and title
models remain cloud models. Selecting Nemotron alone does not make auxiliary
requests or remote MCP tools offline.

## Provisioning and startup

The separately authorized pilot installed TensorFold native **1.2.7** using
`brew install ashhart/tensorfold/tensorfold`. Homebrew also upgraded its CMake
build dependency from 4.4.4 to 4.4.5 and built bundled libjpeg-turbo. The native
engine does not use the Bonsai Python environment. Dotfiles installation does
not install TensorFold or download this checkpoint.

Pinned public checkpoint:

```sh
tensorfold pull TensorFold/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-MLX-4bit@d9d758fb83953437f7263256b0d96157e2a348b8
```

Download includes the MTP head: 17.25 GiB transferred; `tensorfold info` reports
17.27 GiB weights and a 19.27 GiB memory floor. The checkpoint lives under
`~/.cache/huggingface/hub/` by default. The launcher honors `HF_HUB_CACHE` and
`HF_HOME` and serves the exact snapshot directory, avoiding mutable `main`.
Do not delete the shared cache or Bonsai/audio directories.

From this checkout, after provisioning and checking that port 8082 is free:

```sh
bash scripts/serve-nemotron.sh
```

This starts a foreground server on `127.0.0.1:8082`, advertising
`nemotron-lightning`, with 65,536 total tokens, 8,192 maximum output tokens,
one stream, a 0.5 GiB prompt cache, thinking disabled and update checks disabled.
No system memory limits are changed. It does not install or download anything.
Ctrl-C stops the server; run only one large coding/audio model at a time.

In another terminal, select the optional provider:

```sh
opencode run --standalone --model tensorfold/nemotron-lightning \
  'Read README.md and summarize the local model setup.'
```

Or select it through `/models` in a newly started OpenCode session. A pre-existing
background service may retain old settings; the pilot used `--standalone` and
did not restart shared services. Provider sampling sets `temperature: 0` based
on the successful tool test. Server-direct clients must set temperature
explicitly to reproduce those measurements; the server default is 1.0.

The installed `~/.config/opencode/opencode.json` was backed up to
`opencode.json.backup.20261112_232706` alongside it, then changed only by adding
the TensorFold provider. Parsed comparison against that backup confirmed every
pre-existing setting was preserved. Source and installed provider definitions
match. No full AI/shell installation was run. Preserve the backup until satisfied;
rollback should remove only this provider or reconcile the backup with later
customizations, rather than blindly replacing newer settings.

## Measured results

Single stream, native Metal, MTP/copy drafts enabled, thinking off. Other normal
applications remained open. These are synthetic fixtures, not a coding-quality
benchmark or a comparison against Bonsai. Raw pilot evidence is retained locally
under `tests/artifacts/tensorfold-pilot-2026-11-12/`; generated databases and
caches there are not intended for commits.

| Check | Observed result |
| --- | --- |
| Model loading | 19.3 seconds reported by server |
| Short code prompt | 36 input tokens, three 256-token replies; median decode about 266.5 tokens/s; first-token latency 56–75 ms |
| Cold longer prompt | 21,419 input tokens; 5.72 s to first token; correct final-row answer |
| Follow-up | 21,443 input tokens, 21,413 cached; 65 ms to first token; correct answer |
| Larger cold prompt | 55,920 input tokens; 17.56 s to first token; correct answer |
| Over-context input | 66,016 rendered tokens rejected with streamed `context_length_exceeded` error; HTTP status was 200, not 400 |
| Draft/serial comparison | Same 17-token function text and server token hash; about 263 vs 147 tokens/s on this small fixture |
| Structured API tools | Streamed function ID/name/JSON arguments, matching tool result and correct returned value passed in serial, required, sampled and thinking diagnostics |
| OpenCode integration | Installed provider completed a real `read` tool call and answered the fixture value correctly in 6.95 s; explicit read-before-answer variant took 6.59 s |

The 256-token code replies ended at the output cap and contain incomplete code;
their speed does not establish completed-task quality. Longer prompts produced
only five output tokens, so their decode rates are not representative. Cached
follow-up performance depends on available memory and compatible prompt prefixes.
The 55.9K prompt fits alongside the provider's 8K output reserve; this is not a
maximum-output, concurrency, or sustained reliability qualification.

## Memory and limitations

TensorFold's load log reported 19.8 GiB kept wired. The final `/health` physical
footprint reading was **20.79 GiB**; RSS alone was about 3 GiB and substantially
understates Metal allocations. The health `peak` field at this observation is
not an independently sampled high-water mark. System swap was 0.38 MiB before
loading, 3,299.56 MiB immediately after, and roughly 3.1–3.2 GiB during the run.
macOS pressure levels 1 (normal) and 2 (warning) were observed; no critical level
was sampled. TensorFold logged cache shedding under warning pressure.

This is a substantial memory cost on a 36 GiB machine. Treat it as an optional
on-demand backup; stop it after use. Do not increase wired-memory limits to
force a fit. The server was stopped after verification. Swap can remain allocated
after exit and is not evidence that the server is still running.

Failure history is retained:

- The first direct automatic tool request returned an invented ordinary-text
  answer instead of calling the tool. Later diagnostic prompts with a system
  instruction passed; this is prompt sensitivity, not evidence of universal
  tool reliability.
- OpenCode's first normal-sampling fixture run with corrected permissions
  answered incorrectly without calling a tool. Deterministic sampling then
  passed both explicit and ordinary file-read prompts. This does not establish
  general superiority of greedy decoding.
- The initial test's exact absolute permission did not match OpenCode's internal
  workspace-relative read resource. It correctly denied the operation. The test
  allowed the same fixture's relative path; installed permission rules were not
  weakened. All other test-agent actions remained denied.
- OpenCode emitted a stray `</think>` fragment in pre-tool text even with
  thinking disabled. Final fixture answers were correct.
- The initial existing-data run timed out during OpenCode's native V1-to-V2
  history migration. Recovery subsequently completed through the existing
  background service, and a restricted session using normal storage completed
  the Nemotron tool round trip in 3.54 s. No database reset, settings edits or
  service restart was needed. See [startup recovery](opencode-startup-recovery.md).
- The first context-cap probe expected an HTTP 400 and failed its assertion:
  streamed errors use HTTP 200 plus an error event. The saved event proves
  rejection; the original failure was not erased.

The pilot disabled all MCP servers and selected a local title model only through
a temporary per-run overlay. Your normal MCP and title settings are preserved.
It did not establish network-disconnected operation, multi-file implementation
quality, automatic cloud failover, or prolonged stability.

Sources: [TensorFold evaluation](https://github.com/ashhart/TensorFold/blob/main/docs/evaluating.md),
[Nemotron native recipe](https://github.com/ashhart/TensorFold/blob/main/docs/recipes/nemotron-3.5.md),
[checkpoint](https://huggingface.co/TensorFold/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-MLX-4bit),
[API contract](https://github.com/ashhart/TensorFold/blob/main/docs/api.md).
