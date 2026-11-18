"""Utilidades de ffmpeg/Pillow compartidas por los agentes de producción."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def font(size: int) -> ImageFont.ImageFont:
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def run_ffmpeg(args: list[str]) -> None:
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg falló: {' '.join(cmd)}\n{proc.stderr}")


def duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout
    return float(json.loads(out)["format"]["duration"])


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont, max_width: int) -> list[str]:
    lines, line = [], ""
    for word in text.split():
        test = f"{line} {word}".strip()
        if draw.textlength(test, font=fnt) <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_centered(img: Image.Image, text: str, size: int, y_center: int, fill="#FFFFFF", stroke="#000000", max_ratio=0.88) -> None:
    draw = ImageDraw.Draw(img)
    fnt = font(size)
    lines = wrap(draw, text, fnt, int(img.width * max_ratio))
    line_h = int(size * 1.15)
    y = y_center - (line_h * len(lines)) // 2
    for ln in lines:
        w = draw.textlength(ln, font=fnt)
        draw.text(((img.width - w) / 2, y), ln, font=fnt, fill=fill,
                  stroke_width=max(2, size // 12), stroke_fill=stroke)
        y += line_h


def gradient(w: int, h: int, top: str, bottom: str) -> Image.Image:
    t = Image.new("RGB", (1, 1), top).getpixel((0, 0))
    b = Image.new("RGB", (1, 1), bottom).getpixel((0, 0))
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        k = y / max(h - 1, 1)
        c = tuple(int(t[i] * (1 - k) + b[i] * k) for i in range(3))
        for x in range(w):
            px[x, y] = c
    return img
