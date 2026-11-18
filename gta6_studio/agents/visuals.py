"""Rol: Investigador visual. Asigna a cada escena un clip (IA, gameplay propio o tarjeta)."""

from __future__ import annotations

import json
import random
from pathlib import Path

from ..config import Settings
from ..media import draw_centered, duration, gradient
from ..models import Script

VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm"}


def export_ai_prompts(settings: Settings, script: Script, fmt: str, run_id: str, out: Path) -> Path:
    """Exporta los prompts para generar clips con IA (p.ej. Higgsfield, Kling, Seedance)."""
    f = settings["formats"][fmt]
    target = settings.path(settings["visuals"]["ai_clips_dir"]) / run_id
    payload = {
        "instructions": (
            "Genera un clip por escena con estos prompts y guárdalo como "
            f"{target}/scene_XX.mp4 (XX = índice con 2 dígitos). Luego ejecuta: "
            f"python -m gta6_studio render {run_id}"
        ),
        "aspect_ratio": f["aspect"],
        "scenes": [
            {"index": s.index, "file": f"scene_{s.index:02d}.mp4", "prompt": s.ai_video_prompt, "camera": s.camera}
            for s in script.scenes
        ],
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def _footage_index(footage_dir: Path) -> list[Path]:
    if not footage_dir.exists():
        return []
    return sorted(p for p in footage_dir.rglob("*") if p.suffix.lower() in VIDEO_EXT)


def _score(path: Path, keywords: list[str]) -> int:
    name = path.stem.lower().replace("_", " ").replace("-", " ")
    return sum(1 for k in keywords for w in k.lower().split() if w in name)


def _title_card(text: str, w: int, h: int, accent: str, out: Path) -> Path:
    img = gradient(w, h, "#1A0B2E", accent)
    draw_centered(img, text.upper(), size=int(min(w, h) * 0.11), y_center=h // 2)
    img.save(out)
    return out


def run(settings: Settings, script: Script, fmt: str, run_id: str, out_dir: Path) -> list[dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    cfg = settings["visuals"]
    f = settings["formats"][fmt]
    ai_dir = settings.path(cfg["ai_clips_dir"]) / run_id
    footage = _footage_index(settings.path(cfg["footage_dir"]))
    rng = random.Random(run_id)
    used: dict[Path, int] = {}
    plan = []
    for scene in script.scenes:
        ai_clip = ai_dir / f"scene_{scene.index:02d}.mp4"
        if ai_clip.exists():
            plan.append({"index": scene.index, "kind": "ai_clip", "file": str(ai_clip), "start": 0.0})
            continue
        if footage:
            # Mejor coincidencia por nombre de archivo, penalizando repeticiones
            best = max(footage, key=lambda p: (_score(p, scene.footage_keywords) - used.get(p, 0), rng.random()))
            used[best] = used.get(best, 0) + 1
            total = duration(best)
            start = rng.uniform(0, max(0.0, total - 12))
            plan.append({"index": scene.index, "kind": "own_gameplay", "file": str(best), "start": round(start, 2)})
            continue
        card = _title_card(scene.on_screen_text or script.title, f["width"], f["height"],
                           "#FF2D95", out_dir / f"card_{scene.index:02d}.png")
        plan.append({"index": scene.index, "kind": "title_card", "file": str(card), "start": 0.0})
    return plan
