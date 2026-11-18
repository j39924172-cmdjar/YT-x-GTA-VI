"""Rol: Especialista SEO. Título, descripción, etiquetas, capítulos y concepto de miniatura."""

from __future__ import annotations

from ..config import Settings
from ..llm import Brain
from ..models import Script, SeoPackage, ThumbnailPlan
from ._common import GROUND_RULES, channel_brief


def _mock(script: Script) -> SeoPackage:
    return SeoPackage(
        title=script.title[:70],
        description=f"{script.hook}\n\nContenido no oficial. GTA VI es una marca de Rockstar Games.",
        tags=["gta 6", "gta vi", "gta 6 secretos", "vice city", "leonida"],
        hashtags=["#GTA6", "#GTAVI", "#Shorts"],
        chapters=["0:00 Intro"],
        thumbnail=ThumbnailPlan(
            headline="SECRETO OCULTO",
            image_prompt="Neon tropical city skyline at dusk, dramatic lighting, cinematic",
            color_accent="#FF2D95",
        ),
    )


def run(settings: Settings, brain: Brain, script: Script, fmt: str, scene_times: list[float]) -> SeoPackage:
    timeline = "\n".join(
        f"{int(t // 60)}:{int(t % 60):02d} escena {i}: {s.on_screen_text}"
        for i, (t, s) in enumerate(zip(scene_times, script.scenes))
    )
    return brain.structured(
        system=(
            "Eres especialista en SEO de YouTube para gaming en español. Optimizas para búsqueda y CTR "
            "sin prometer nada que el vídeo no cumpla.\n\n" + GROUND_RULES
        ),
        prompt=(
            f"{channel_brief(settings)}\n\nGuion final:\n{script.model_dump_json(indent=2)}\n\n"
            f"Formato: {fmt}. Marcas de tiempo reales:\n{timeline}\n\n"
            "Genera: título (máx 70 caracteres), descripción (primeras 2 líneas con la keyword, "
            "aviso 'contenido no oficial / fan-made', fuentes), 15-25 etiquetas, 3-5 hashtags "
            "(incluye #Shorts si es short), capítulos con las marcas de tiempo reales (solo si es long) "
            "y el plan de miniatura (texto de 2-4 palabras, prompt de imagen original sin personajes ni logos de Rockstar)."
        ),
        schema=SeoPackage,
        mock=lambda: _mock(script),
    )
