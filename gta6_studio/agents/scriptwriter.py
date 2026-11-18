"""Rol: Guionista + director de arte. Escribe el guion escena a escena y los prompts visuales."""

from __future__ import annotations

from ..config import Settings
from ..llm import Brain
from ..models import Scene, Script, VideoIdea
from ._common import GROUND_RULES, channel_brief

WORDS_PER_SECOND = 2.6  # ritmo de locución en español


def _mock(idea: VideoIdea, n: int) -> Script:
    scenes = [
        Scene(
            index=i,
            narration=(idea.hook if i == 0 else f"Este es el punto número {i} del vídeo, con un dato interesante sobre GTA 6."),
            on_screen_text=("SECRETO #%d" % i) if i else "¿LO SABÍAS?",
            visual_description="Plano aéreo de Vice City al atardecer",
            footage_keywords=["vice city", "atardecer"],
            ai_video_prompt="Cinematic aerial shot of a neon-lit tropical city at sunset, palm trees, ocean, 4k",
            camera="drone lento hacia delante",
        )
        for i in range(n)
    ]
    return Script(
        title=idea.working_title,
        hook=idea.hook,
        scenes=scenes,
        call_to_action="Suscríbete para más secretos de GTA 6",
        sources_note="(dry-run)",
    )


def run(settings: Settings, brain: Brain, idea: VideoIdea, fmt: str) -> Script:
    f = settings["formats"][fmt]
    words = int(f["target_seconds"] * WORDS_PER_SECOND)
    return brain.structured(
        system=(
            "Eres guionista y director de arte de un canal de YouTube sobre GTA 6. "
            "Escribes para la voz: frases cortas, ritmo alto, un giro cada 15-20 segundos, "
            "y un gancho en los primeros 3 segundos.\n\n" + GROUND_RULES
        ),
        prompt=(
            f"{channel_brief(settings)}\n\nIdea aprobada:\n{idea.model_dump_json(indent=2)}\n\n"
            f"Formato: {fmt}, relación {f['aspect']}, unas {words} palabras de narración en total, "
            f"exactamente {f['scenes']} escenas (index desde 0). La escena 0 es el gancho; la última incluye la llamada a la acción.\n"
            "Para cada escena:\n"
            "- narration: texto exacto a locutar en el idioma del canal.\n"
            "- footage_keywords: 2-4 palabras para encontrar gameplay propio que encaje.\n"
            "- ai_video_prompt: prompt en inglés para un generador de vídeo IA (Seedance/Kling/Higgsfield). "
            "Describe una escena ORIGINAL inspirada en la estética de Florida/Miami tropical y neón; "
            "NO pidas personajes, logotipos ni marcas de Rockstar.\n"
            "En sources_note resume qué datos vienen de fuentes y cuáles son rumores."
        ),
        schema=Script,
        mock=lambda: _mock(idea, f["scenes"]),
    )
