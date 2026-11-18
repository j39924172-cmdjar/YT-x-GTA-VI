"""Rol: Responsable de cumplimiento. Revisa derechos, políticas de YouTube y veracidad antes de publicar."""

from __future__ import annotations

from ..config import Settings
from ..llm import Brain
from ..models import ComplianceReport, Script, SeoPackage
from ._common import GROUND_RULES


def _mock() -> ComplianceReport:
    return ComplianceReport(approved=True, synthetic_media_disclosure_needed=True, issues=[])


def run(settings: Settings, brain: Brain, script: Script, seo: SeoPackage, visual_sources: dict[int, str]) -> ComplianceReport:
    return brain.structured(
        system=(
            "Eres el responsable de cumplimiento de un canal de YouTube. Revisas antes de publicar:\n"
            "1) Derechos: uso de material de Rockstar (permitido comentar/analizar gameplay propio; "
            "no subir tráileres o música oficial íntegros; no suplantar a Rockstar).\n"
            "2) Políticas de YouTube: contenido sintético realista debe declararse; spam/contenido repetitivo; "
            "metadatos engañosos; anuncios aptos.\n"
            "3) Veracidad: rumores presentados como hechos.\n"
            "Marca 'block' solo para problemas que impidan publicar; 'warn' para mejoras.\n\n" + GROUND_RULES
        ),
        prompt=(
            f"Guion:\n{script.model_dump_json(indent=2)}\n\nSEO:\n{seo.model_dump_json(indent=2)}\n\n"
            f"Origen del vídeo por escena (gameplay propio / clip IA / tarjeta): {visual_sources}\n\n"
            "Devuelve el informe. approved=false si hay algún 'block'."
        ),
        schema=ComplianceReport,
        mock=_mock,
    )
