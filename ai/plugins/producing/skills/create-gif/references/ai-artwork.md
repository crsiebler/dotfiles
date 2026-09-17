# Optional AI artwork for GIFs

Use this route only when the user requests original generated artwork. Supplied
frames and procedural graphics stay independent of providers. Identify whether the
user wants an object moved as a whole, a visual effect, or articulated character
motion before choosing generation work.

## Capability and routing decision

Inspect the tools actually exposed by the active runtime, including input-image,
output-file, frame-sheet, and editing capabilities. A installed CLI, an OpenCode
plugin name, or a provider mentioned in documentation does not make its tool
available in Codex. Do not invent names, arguments, output paths, costs, or quotas.

For pixel art, load the advertised `create-sprites` skill and use its asset contract,
frame-grid/anchor guidance, provider boundaries, and validation workflow. Resolve
it through skill discovery, never a sibling Python import or guessed cache path.
Its current documented provider is OpenCode-specific; if that loaded workflow
cannot use the active provider, report that concrete limitation and offer planning
or supplied-frame assembly. Do not bypass it with procedural substitute artwork.
Asset-only GIF work does not require a game engine or project.godot.

For illustration or other non-pixel artwork, use a suitable available image tool
according to its active schema and instructions. Establish the intended batch,
reference images, canvas, pose list, palette/style, common anchor, background, and
output location from the request. Carry forward existing authorization; obtain only
missing generation/spending approval required by the selected tool/workflow. Do not
launch generation simply because this skill was selected, and do not retry beyond
the approved scope.

If no suitable provider is available, say what is unavailable. Offer an asset plan,
assembly of supplied art, or the documented procedural route when it matches the
user's intent. Do not install a provider, claim generated art exists, or quietly
replace requested articulated artwork with a translated static image.

## Motion and frame construction

A single static image can support translation, rotation, zoom, or effects using
explicitly chosen project-local image operations. Describe it as motion of a static
image. Walking, gesturing, blinking, and changing limb/body poses need distinct
coherent frames; request a pose sequence or aligned frame sheet when the provider
supports it. A still-image generator does not imply video or temporal consistency.

Inspect generated source images before processing. Verify actual canvas dimensions,
frame count/grid, frame order, and each cell's content; prompts are not evidence
that a returned sheet obeys the contract. Use the available image inspection tool,
not dimensions alone. Preserve the original source and select crop boxes from the
observed grid. If tool outputs are outside the project, use only an authorized
copy/import into the project; never mutate provider-managed or installed resources.

For each frame, check the same scale, palette/style, shared anchor/baseline, and
background/alpha policy. Crop on a consistent grid, normalize the canvas around one
anchor, and check that no limb is clipped or duplicated. Preserve aspect ratio;
nearest sampling is for pixel art. Do not stretch individual poses to disguise
inconsistent generation. Use separate files for extracted frames so the supplied-
frame assembler can validate static inputs.

## Assembly, review, and delivery

Create the project request described in [authoring.md](authoring.md) with explicit
per-frame timing and loop/background choices. Encode with the existing assembler;
verify decoded metadata with `inspect`. Review representative frames, the entire
sequence when playback is available, and the last-to-first transition. Check for
flicker, anchor jumps, style drift, accidental holds, transparent trails, and timing
that fits the action. Correct deterministic extraction/alignment problems without
regenerating artwork; regenerate only an approved failed source when needed.

Report which source/frame and playback inspections actually happened. If a visual
inspection capability or playback is unavailable, label that remaining limitation;
structural validation is not visual approval. Deliver project artifact paths,
actual decoded size/timing/loop metadata, provenance, and any remaining defects.
Distinguish supplied art, procedural graphics, static-image motion, and articulated
AI frames honestly. Never claim instruction evaluations were live generation tests.
