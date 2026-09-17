"""Adapted from Anthropic slack-gif-creator core/gif_builder.py, Apache-2.0.
Modified 2026-09-17: Pillow-only encoding, aspect-preserving fit, accumulated
frame timing, explicit alpha/disposal policy, and decoded output verification.
See ../LICENSE.txt and ../references/provenance.md.
"""
import io
from PIL import Image, ImageOps
from gif_files import GifError


class GIFBuilder:
    def __init__(self, width=256, height=256, sampling='nearest', background='#ffffff'):
        self.size = (width, height)
        self.sampling = Image.Resampling.NEAREST if sampling == 'nearest' else Image.Resampling.LANCZOS
        self.background = background
        self.frames = []
        self.durations = []
        self.requested_duration = 0

    def add_frame(self, frame, duration):
        fitted = ImageOps.contain(frame.convert('RGBA'), self.size, self.sampling)
        color = (0, 0, 0, 0) if self.background == 'transparent' else self.background
        canvas = Image.new('RGBA', self.size, color)
        canvas.alpha_composite(fitted, ((self.size[0] - fitted.width) // 2,
                                       (self.size[1] - fitted.height) // 2))
        self.frames.append(canvas)
        self.durations.append(((duration + 5) // 10) * 10)
        self.requested_duration += duration

    def reduce_frames(self, stride):
        frames, durations = [], []
        for start in range(0, len(self.frames), stride):
            frames.append(self.frames[start])
            durations.append(sum(self.durations[start:start + stride]))
        self.frames, self.durations = frames, durations
        self.deduplicate_frames()

    def deduplicate_frames(self):
        frames, durations = [], []
        previous = None
        for frame, duration in zip(self.frames, self.durations):
            pixels = frame.tobytes()
            if pixels == previous:
                durations[-1] += duration
            else:
                frames.append(frame)
                durations.append(duration)
                previous = pixels
        if any(d > 655350 for d in durations):
            raise GifError(2, 'input: merged duration exceeds GIF limit')
        self.frames, self.durations = frames, durations

    def optimize_colors(self, colors):
        # Sample every frame at bounded resolution to form one shared palette.
        samples = []
        for frame in self.frames:
            sample = frame.convert('RGB')
            sample.thumbnail((64, 64), Image.Resampling.NEAREST)
            samples.append(sample)
        strip = Image.new('RGB', (64, 64 * len(samples)))
        for index, sample in enumerate(samples):
            strip.paste(sample, (0, 64 * index))
        transparent = self.background == 'transparent'
        palette = strip.quantize(colors=min(colors, 255) if transparent else colors)
        result = []
        for frame in self.frames:
            quantized = frame.convert('RGB').quantize(palette=palette, dither=Image.Dither.NONE)
            if transparent:
                # The sampled palette reserves its unused final index for alpha.
                mask = frame.getchannel('A').point(lambda alpha: 255 if alpha < 128 else 0)
                quantized.paste(255, mask=mask)
                quantized.info['transparency'] = 255
            result.append(quantized)
        return result

    def encode(self, colors, loop, max_bytes):
        frames = self.optimize_colors(colors)
        stream = io.BytesIO()
        options = dict(save_all=True, append_images=frames[1:], duration=self.durations,
                       disposal=2, optimize=False)
        if loop is not None:
            options['loop'] = loop
        if self.background == 'transparent':
            options.update(transparency=255, background=255)
        frames[0].save(stream, format='GIF', **options)
        content = stream.getvalue()
        if len(content) > max_bytes:
            raise GifError(5, 'validation: GIF exceeds requested byte limit')
        info = inspect_gif(io.BytesIO(content), len(content))
        if (info['duration_ms'] != sum(self.durations) or info['loop'] != loop
                or info['dimensions'] != list(self.size)):
            raise GifError(5, 'validation: decoded GIF differs from encoding contract')
        info['requested_duration_ms'] = self.requested_duration
        return content, info


def inspect_gif(source, size_bytes):
    durations, disposals = [], []
    with Image.open(source) as image:
        if image.format != 'GIF':
            raise GifError(2, 'input: expected GIF format')
        dimensions = list(image.size)
        if image.width * image.height > 4096 * 4096:
            raise GifError(2, 'input: GIF canvas exceeds inspection limit')
        loop = image.info.get('loop')
        for index in range(201):
            try:
                image.seek(index)
            except EOFError:
                break
            if index == 200 or (index + 1) * image.width * image.height > 32_000_000:
                raise GifError(2, 'input: GIF frame/pixel inspection limit exceeded')
            image.load()
            durations.append(image.info.get('duration', 0))
            disposals.append(image.disposal_method)
    return dict(format='GIF', dimensions=dimensions, size_bytes=size_bytes,
                frame_count=len(durations), durations_ms=durations,
                duration_ms=sum(durations), loop=loop, disposal=disposals)
