#!/usr/bin/env python3
"""Project-bounded supplied-frame and procedural GIF creation and inspection."""
import argparse
import json
from pathlib import Path
import re
import sys
import warnings
sys.dont_write_bytecode = True
from gif_files import GifError, no_links, project_path, publish


def integer(value, low, high, label):
    if type(value) is not int or not low <= value <= high:
        raise GifError(2, f'input: {label} must be an integer in {low}..{high}')
    return value


def color(value, *, transparent=False):
    if transparent and value == 'transparent':
        return value
    if not isinstance(value, str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', value):
        raise GifError(2, 'input: colors must be #RRGGBB (or supported transparent background)')
    return value


def generate(root, spec, action):
    from PIL import Image
    from gif_builder import GIFBuilder
    from frame_composer import orbit_frames
    common = {'width', 'height', 'colors', 'sampling', 'background', 'loop', 'reduce_every', 'max_bytes'}
    special = {'frames', 'durations_ms'} if action == 'assemble' else {'frame_count', 'duration_ms', 'radius', 'foreground'}
    if not isinstance(spec, dict) or set(spec) - common - special:
        raise GifError(2, 'input: expected request object with supported fields')
    width = integer(spec.get('width', 256), 1, 1024, 'width')
    height = integer(spec.get('height', 256), 1, 1024, 'height')
    colors = integer(spec.get('colors', 128), 2, 256, 'colors')
    sampling = spec.get('sampling', 'nearest')
    if sampling not in ('nearest', 'lanczos'):
        raise GifError(2, 'input: sampling must be nearest or lanczos')
    background = color(spec.get('background', '#ffffff'), transparent=True)
    loop = spec.get('loop', 0)
    if loop is not None:
        integer(loop, 0, 65535, 'loop')
    stride = integer(spec.get('reduce_every', 1), 1, 200, 'reduce_every')
    max_bytes = integer(spec.get('max_bytes', 10485760), 1, 10485760, 'max_bytes')
    builder = GIFBuilder(width, height, sampling, background)
    if action == 'assemble':
        frames, durations = spec.get('frames'), spec.get('durations_ms')
        if (not isinstance(frames, list) or not 1 <= len(frames) <= 200
                or not isinstance(durations, list) or len(durations) != len(frames)):
            raise GifError(2, 'input: provide 1..200 frames and matching durations_ms')
        if width * height * len(frames) > 32_000_000:
            raise GifError(2, 'input: target pixel budget exceeded')
        pixels = 0
        for file, duration in zip(frames, durations):
            integer(duration, 10, 655350, 'duration_ms')
            path = project_path(root, file)
            with Image.open(path) as image:
                pixels += image.width * image.height
                if (image.width > 4096 or image.height > 4096 or pixels > 32_000_000
                        or getattr(image, 'n_frames', 1) != 1):
                    raise GifError(2, 'input: source dimension/frame/pixel limit exceeded')
                builder.add_frame(image, duration)
    else:
        count = integer(spec.get('frame_count', 24), 2, 200, 'frame_count')
        duration = integer(spec.get('duration_ms', 80), 10, 655350, 'duration_ms')
        radius = integer(spec.get('radius', max(1, min(width, height) // 8)),
                         1, max(1, (min(width, height) - 2) // 2), 'radius')
        if min(width, height) < 4 or width * height * count > 32_000_000:
            raise GifError(2, 'input: procedural canvas/pixel limit exceeded')
        foreground = color(spec.get('foreground', '#e04040'))
        for frame in orbit_frames(width, height, count, radius, foreground):
            builder.add_frame(frame, duration)
    builder.reduce_frames(stride)
    return builder.encode(colors, loop, max_bytes)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path)
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('check')
    sub.add_parser('inspect').add_argument('input')
    for action in ('assemble', 'procedural'):
        command = sub.add_parser(action)
        command.add_argument('input')
        command.add_argument('output')
    args = parser.parse_args()
    try:
        try:
            from PIL import Image, UnidentifiedImageError, __version__
        except ImportError:
            raise GifError(3, 'dependency: Pillow required; see references/requirements.md') from None
        warnings.simplefilter('error', Image.DecompressionBombWarning)
        if sys.version_info < (3, 11):
            raise GifError(3, 'dependency: Python 3.11 or newer required')
        if args.action == 'check':
            print(json.dumps({'python': sys.version.split()[0], 'Pillow': __version__}))
            return 0
        if args.project is None:
            raise GifError(2, 'input: --project is required')
        no_links(args.project.absolute())
        root = args.project.resolve()
        if not root.is_dir():
            raise GifError(2, 'input: project directory does not exist')
        source = project_path(root, args.input)
        from gif_builder import inspect_gif
        try:
            if args.action == 'inspect':
                info = inspect_gif(source, source.stat().st_size)
            else:
                output = project_path(root, args.output, output=True)
                if source.stat().st_size > 65536:
                    raise GifError(2, 'input: request exceeds 64 KiB')
                try:
                    spec = json.loads(source.read_text(encoding='utf-8'))
                except (ValueError, UnicodeError, RecursionError):
                    raise GifError(2, 'input: invalid JSON request') from None
                content, info = generate(root, spec, args.action)
                publish(output, content)
        except (UnidentifiedImageError, Image.DecompressionBombWarning, Image.DecompressionBombError):
            raise GifError(2, 'input: unsupported or oversized image') from None
        print(json.dumps(info))
        return 0
    except GifError as error:
        print(str(error), file=sys.stderr)
        return error.code
    except (OSError, ValueError, TypeError, OverflowError):
        print('generation: image operation failed; check inputs and filesystem access', file=sys.stderr)
        return 4


if __name__ == '__main__':
    sys.exit(main())
