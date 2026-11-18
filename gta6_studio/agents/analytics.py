"""Rol: Analista. Mide qué funciona y alimenta al scout y al estratega en la siguiente ronda."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from ..config import Settings

log = logging.getLogger(__name__)


def _history_file(settings: Settings) -> Path:
    return settings.data_dir / "history.json"


def load(settings: Settings) -> list[dict]:
    f = _history_file(settings)
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else []


def record(settings: Settings, entry: dict) -> None:
    hist = load(settings)
    hist.append({**entry, "created_at": datetime.now(timezone.utc).isoformat()})
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    _history_file(settings).write_text(json.dumps(hist, ensure_ascii=False, indent=2), encoding="utf-8")


def refresh_stats(settings: Settings) -> list[dict]:
    """Actualiza visitas/likes/comentarios de los vídeos publicados."""
    hist = load(settings)
    ids = [h["video_id"] for h in hist if h.get("video_id")]
    if not ids or settings.dry_run:
        return hist
    from .publisher import youtube_client

    yt = youtube_client(settings)
    stats = {}
    for i in range(0, len(ids), 50):
        res = yt.videos().list(part="statistics", id=",".join(ids[i:i + 50])).execute()
        stats.update({it["id"]: it["statistics"] for it in res.get("items", [])})
    for h in hist:
        if h.get("video_id") in stats:
            h["stats"] = stats[h["video_id"]]
    _history_file(settings).write_text(json.dumps(hist, ensure_ascii=False, indent=2), encoding="utf-8")
    return hist


def summary(settings: Settings, last: int = 20) -> str:
    hist = load(settings)[-last:]
    if not hist:
        return "Sin historial todavía (canal nuevo)."
    lines = []
    for h in hist:
        s = h.get("stats", {})
        lines.append(
            f"- [{h.get('format')}] {h.get('title')} | pilar: {h.get('pillar')} | "
            f"vistas: {s.get('viewCount', '?')} likes: {s.get('likeCount', '?')} comentarios: {s.get('commentCount', '?')}"
        )
    return "\n".join(lines)
