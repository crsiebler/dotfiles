"""Adapted from Anthropic slack-gif-creator core/frame_composer.py, Apache-2.0.
Modified 2026-09-17: Pillow-only periodic circle fixture; removed NumPy/text helpers.
See ../LICENSE.txt. The procedural path needs no fonts or image provider.
"""
import math
from PIL import Image, ImageDraw


def orbit_frames(width, height, count, radius, foreground):
    for index in range(count):
        phase = 2 * math.pi * index / count
        x = width / 2 + (width / 2 - radius - 1) * math.cos(phase)
        y = height / 2 + (height / 2 - radius - 1) * math.sin(phase)
        frame = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        ImageDraw.Draw(frame).ellipse((x - radius, y - radius, x + radius, y + radius),
                                     fill=foreground)
        yield frame
