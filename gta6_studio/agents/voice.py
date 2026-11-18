"""Rol: Locutor. Convierte la narración de cada escena en audio (ElevenLabs)."""

from __future__ import annotations

import logging
from pathlib import Path

import requests

from ..config import Settings
from ..media import duration, run_ffmpeg
from ..models import Script
from .scriptwriter import WORDS_PER_SECOND

log = logging.getLogger(__name__)


def _elevenlabs(text: str, out: Path, api_key: str, voice_id: str, model_id: str) -> None:
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={"xi-api-key": api_key, "Accept": "audio/mpeg"},
        json={"text": text, "model_id": model_id},
        timeout=120,
    )
    r.raise_for_status()
    out.write_bytes(r.content)


def _silent(text: str, out: Path) -> None:
    secs = max(1.5, len(text.split()) / WORDS_PER_SECOND)
    run_ffmpeg(["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", f"{secs:.2f}", "-q:a", "4", str(out)])


def run(settings: Settings, script: Script, out_dir: Path) -> list[dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    cfg = settings["voice"]
    api_key, voice_id = settings.env("ELEVENLABS_API_KEY"), settings.env("ELEVENLABS_VOICE_ID")
    use_tts = cfg["provider"] == "elevenlabs" and not settings.dry_run
    if use_tts and not (api_key and voice_id):
        raise RuntimeError("Faltan ELEVENLABS_API_KEY / ELEVENLABS_VOICE_ID (o usa voice.provider: silent)")

    results = []
    for scene in script.scenes:
        out = out_dir / f"scene_{scene.index:02d}.mp3"
        if use_tts:
            _elevenlabs(scene.narration, out, api_key, voice_id, cfg["model_id"])
        else:
            _silent(scene.narration, out)
        results.append({"index": scene.index, "file": str(out), "seconds": duration(out)})
        log.info("Voz escena %d: %.1fs", scene.index, results[-1]["seconds"])
    return results
