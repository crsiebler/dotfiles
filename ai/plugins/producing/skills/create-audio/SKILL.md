---
name: create-audio
description: Generate audio through backend adapters using project-owned prompts and settings. Currently supports sound effects and ambience with Stable Audio MLX.
---

# Create Audio

Use the bundled `scripts/create_audio.py` with Python 3.11+. Resolve its path
relative to this installed skill, not a dotfiles checkout or another project's
wrapper. Agents interact through this skill; OpenCode's optional `/create-audio`
command loads it. No shell alias or chat-model provider is involved.

The currently implemented Stable Audio runtime defaults to `~/Models/local-audio/`, overridden by
`LOCAL_AUDIO_MODELS_ROOT` or `--models-root`. It contains pinned source,
environments, and weights only. Project prompts and generation preferences do
not belong there. This backend generates SFX and ambience, not speech or music;
ACE-Step remains a separate workflow.

1. Read the active project's asset instructions and applicable artistic briefs,
   contracts, batch authorization, and review requirements. For New Zion, these
   include its sonic bible, cue catalog, family approvals, and runtime gates.
   Do not assume those requirements apply to other projects.
2. Read [request format and backend setup](references/local-audio.md). Create or
   use a project-local request with explicit settings. Derive the prompt and
   negative prompt from the project, not a personal default. Preserve existing
   batch authorization; do not request repeated approval for the same scope.
3. For Stable Audio, run `status` to check pinned source and weight integrity. This check does not
   demonstrate working Python dependencies, performance, or audible quality.
   Setup is separate from generation; do not install or download implicitly.
4. Preview `generate --project-root <project> --request <request.json> --dry-run`.
   Invoke generation only for the authorized batch. The Stable Audio adapter runs
   offline and writes raw float WAV audio. The shared workflow records provenance
   and preserves failures; use a new filename for retries. Hosted adapters are
   not implemented; do not assume network access, credentials, or spending
   authorization from this extension point.
5. Follow project processing and review requirements. Preserve raw sources;
   derive masters and runtime formats separately. A seed does not guarantee
   identical output across runtime or hardware changes. Technical checks do not
   substitute for listening approval.

Asset-only generation needs no game engine. Load and validate engine resources
only when requested by the project. Report paths, settings, hashes, processing,
checks performed, and any remaining quality or integration work.
