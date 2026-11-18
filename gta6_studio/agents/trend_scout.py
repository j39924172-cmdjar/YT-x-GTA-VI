"""Rol: Scout de tendencias. Detecta de qué se está hablando AHORA sobre GTA 6."""

from __future__ import annotations

import logging
from datetime import date

import requests

from ..config import Settings
from ..llm import Brain
from ..models import TrendItem, TrendReport
from ._common import channel_brief

log = logging.getLogger(__name__)


def _youtube_trending(api_key: str, max_results: int = 15) -> list[str]:
    """Vídeos recientes más vistos sobre GTA 6 (YouTube Data API v3)."""
    published_after = date.today().replace(day=1).isoformat() + "T00:00:00Z"
    r = requests.get(
        "https://www.googleapis.com/youtube/v3/search",
        params={
            "part": "snippet",
            "q": "GTA 6",
            "type": "video",
            "order": "viewCount",
            "publishedAfter": published_after,
            "maxResults": max_results,
            "key": api_key,
        },
        timeout=30,
    )
    r.raise_for_status()
    return [
        f"{it['snippet']['title']} — {it['snippet']['channelTitle']}"
        for it in r.json().get("items", [])
    ]


def _reddit_hot(limit: int = 15) -> list[str]:
    try:
        r = requests.get(
            "https://www.reddit.com/r/GTA6/hot.json",
            params={"limit": limit},
            headers={"User-Agent": "gta6-studio/0.1"},
            timeout=30,
        )
        r.raise_for_status()
        return [c["data"]["title"] for c in r.json()["data"]["children"]]
    except requests.RequestException as e:
        log.warning("Reddit no disponible: %s", e)
        return []


def _mock() -> TrendReport:
    return TrendReport(
        summary="(dry-run) Tendencias de ejemplo sobre GTA 6.",
        items=[
            TrendItem(topic="Secretos del mapa de Leonida", why_now="Los jugadores siguen descubriendo zonas", source="mock", heat=9),
            TrendItem(topic="Mejores formas de ganar dinero rápido", why_now="Búsquedas en alza", source="mock", heat=8),
            TrendItem(topic="Teorías sobre el final de Lucia y Jason", why_now="Debate en Reddit", source="mock", heat=7),
        ],
    )


def run(settings: Settings, brain: Brain, history_note: str) -> TrendReport:
    signals: list[str] = []
    if not settings.dry_run:
        if key := settings.env("YOUTUBE_API_KEY"):
            try:
                signals += [f"[YouTube] {t}" for t in _youtube_trending(key)]
            except requests.RequestException as e:
                log.warning("YouTube API no disponible: %s", e)
        signals += [f"[Reddit r/GTA6] {t}" for t in _reddit_hot()]

    system = (
        "Eres el scout de tendencias de un canal de YouTube sobre GTA 6. "
        "Investigas en la web noticias, actualizaciones, descubrimientos de la comunidad y búsquedas en alza."
    )
    prompt = (
        f"{channel_brief(settings)}\n\nFecha de hoy: {date.today().isoformat()}\n\n"
        "Señales recogidas automáticamente:\n" + ("\n".join(signals) or "(ninguna)") + "\n\n"
        f"Rendimiento histórico del canal:\n{history_note}\n\n"
        "Busca en la web lo más relevante sobre GTA 6 de los últimos 7 días (noticias de Rockstar, "
        "parches, descubrimientos virales, rumores con su grado de fiabilidad). "
        "Devuelve un informe con los 8-10 temas con más potencial, indicando la fuente de cada uno."
    )
    notes = brain.research(system, prompt, mock=lambda: "(dry-run)")
    return brain.structured(
        system="Conviertes notas de investigación en un informe estructurado.",
        prompt=f"Notas de investigación:\n{notes}\n\nEstructura el informe de tendencias.",
        schema=TrendReport,
        mock=_mock,
    )
