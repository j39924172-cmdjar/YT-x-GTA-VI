"""Rol: Diseñador de miniaturas. Compone la miniatura 1280x720 con texto de alto contraste."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

from ..media import draw_centered, gradient, run_ffmpeg
from ..models import ThumbnailPlan

W, H = 1280, 720


def _background(plan_items: list[dict], ai_bg: Path | None, work: Path) -> Image.Image:
    if ai_bg and ai_bg.exists():
        return Image.open(ai_bg).convert("RGB")
    for item in plan_items:
        if item["kind"] in ("ai_clip", "own_gameplay"):
            frame = work / "thumb_frame.jpg"
            run_ffmpeg(["-ss", str(item["start"] + 1), "-i", item["file"], "-frames:v", "1", str(frame)])
            return Image.open(frame).convert("RGB")
    return gradient(W, H, "#1A0B2E", "#FF2D95")


def _cover(img: Image.Image) -> Image.Image:
    scale = max(W / img.width, H / img.height)
    img = img.resize((int(img.width * scale) + 1, int(img.height * scale) + 1))
    left, top = (img.width - W) // 2, (img.height - H) // 2
    return img.crop((left, top, left + W, top + H))


def run(plan: ThumbnailPlan, plan_items: list[dict], work: Path, ai_bg: Path | None = None) -> Path:
    img = _cover(_background(plan_items, ai_bg, work))
    img = ImageEnhance.Contrast(ImageEnhance.Color(img).enhance(1.35)).enhance(1.15)
    # Viñeta inferior para que el texto destaque
    mask = Image.linear_gradient("L").resize((W, H))
    img = Image.composite(Image.new("RGB", (W, H), "black"), img, mask.point(lambda v: int(v * 0.75)))
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=80))
    draw_centered(img, plan.headline.upper(), size=118, y_center=int(H * 0.72), fill=plan.color_accent, max_ratio=0.92)
    out = work / "thumbnail.jpg"
    img.save(out, quality=92)
    return out
