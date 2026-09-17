# GIF inputs and encoding contract

Invoke `python /loaded/create-gif/scripts/create_gif.py` from any directory:

- `check`: report Python/Pillow versions without generation.
- `--project ROOT assemble REQUEST.json OUTPUT.gif`: supplied frames.
- `--project ROOT procedural REQUEST.json OUTPUT.gif`: a looping moving circle.
- `--project ROOT inspect INPUT.gif`: decoded metadata only.

All paths resolve under existing ROOT. Reject symlinks, escaping paths, installed
resource outputs, and existing output paths; output parents must already exist.
No installation, download, provider, or server is started. Exit codes: 0 success,
2 input, 3 dependency, 4 generation/I/O, 5 output validation.

Requests are JSON objects (at most 64 KiB) with width/height (1–1024), durations_ms
(one integer per supplied frame, each 10–655350), loop (0 infinite; 1–65535 repeat
count; null omit looping extension), colors (2–256), sampling (nearest or lanczos),
background (#RRGGBB or transparent), reduce_every (positive integer, default 1),
and max_bytes (1–10485760, default 10485760). Defaults: 256x256, 128 colors,
nearest sampling, white background, infinite loop. Unknown keys are errors.

For assemble, frames is a nonempty list of project-relative static image paths,
with at most 200 entries. Each image must contain one frame; animated inputs need
explicit extraction elsewhere. Fit each image inside the requested canvas while
preserving aspect ratio; center and pad. Nearest preserves pixel-art edges;
lanczos is appropriate for photographic artwork. Total decoded source and target
pixels must each stay within 32 million; each source is at most 4096x4096 and
10 MiB. Pillow decompression warnings are treated as input errors.

For procedural, use frame_count (2–200), duration_ms (10–655350), foreground
(#RRGGBB), and radius (positive, fits canvas). A circle traverses a periodic orbit;
frames sample [0, 1), avoiding a duplicated endpoint. No fonts required.

Timing rounds each supplied duration to the nearest 10 ms (half rounds upward),
then reduction holds the first frame of each consecutive group for the group's
summed duration. Exact consecutive duplicate images merge by adding duration;
no near-duplicate threshold discards subtle motion. A group over GIF's 655350 ms
limit fails. Report requested and encoded totals separately; viewers may clamp
short durations, so encoded time does not guarantee playback time.

Use a shared sampled palette without dithering. Solid background composites RGBA
before quantization. Transparent background thresholds alpha at 128; semitransparent
pixels are not representable in GIF. Reserve index 255 for transparency, so at most
255 opaque colors remain. Use disposal 2 and full canvases to clear previous frame
content; optimize is disabled to keep palette/transparency policy predictable.
Palette sampling and GIF's limited colors are lossy; inspect appearance separately.

Encode in memory, reopen and inspect every decoded frame's duration, dimensions,
format, frame count, loop, and disposal. Reject unexpected duration/loop/dimensions
or size excess before publishing a fresh output. Inspection reports actual bytes,
per-frame durations, and total elapsed time, not a guessed frame count / FPS.
