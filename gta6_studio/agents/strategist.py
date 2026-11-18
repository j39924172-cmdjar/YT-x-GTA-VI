"""Rol: Estratega de contenido. Elige la idea con más potencial."""

from __future__ import annotations

from ..config import Settings
from ..llm import Brain
from ..models import IdeaSlate, TrendReport, VideoIdea
from ._common import GROUND_RULES, channel_brief


def _mock(fmt: str) -> IdeaSlate:
    return IdeaSlate(
        chosen_index=0,
        ideas=[
            VideoIdea(
                working_title="5 secretos de Leonida que casi nadie ha visto",
                angle="Lugares ocultos con ubicación exacta",
                hook="¿Sabías que en Vice City hay un lugar al que solo se llega de noche?",
                pillar="secretos, easter eggs y detalles ocultos de Leonida / Vice City",
                target_format=fmt,  # type: ignore[arg-type]
                why_it_will_perform="Alto interés de búsqueda y retención por listas",
                facts_to_verify=["Ubicaciones exactas de cada secreto"],
            )
        ],
    )


def run(settings: Settings, brain: Brain, trends: TrendReport, fmt: str, history_note: str, topic: str | None) -> VideoIdea:
    forced = f"\nEl productor ha pedido este tema concreto: {topic}\n" if topic else ""
    slate = brain.structured(
        system=(
            "Eres el estratega de contenido de un canal de YouTube sobre GTA 6. "
            "Maximizas CTR y retención sin engañar. Piensas en lo que la audiencia buscará hoy.\n\n"
            + GROUND_RULES
        ),
        prompt=(
            f"{channel_brief(settings)}\n\nInforme de tendencias:\n{trends.model_dump_json(indent=2)}\n\n"
            f"Rendimiento histórico (evita repetir temas recientes, potencia lo que funciona):\n{history_note}\n"
            f"{forced}\nFormato objetivo: {fmt} ({settings['formats'][fmt]['target_seconds']} s).\n"
            "Propón 5 ideas distintas y elige la mejor en chosen_index."
        ),
        schema=IdeaSlate,
        mock=lambda: _mock(fmt),
    )
    idx = min(max(slate.chosen_index, 0), len(slate.ideas) - 1)
    return slate.ideas[idx]
