"""Esquemas de datos que se pasan entre los agentes del equipo."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Strict(BaseModel):
    # additionalProperties: false -> válido para salidas estructuradas de Claude
    model_config = ConfigDict(extra="forbid")


class TrendItem(Strict):
    topic: str
    why_now: str
    source: str
    heat: int = Field(description="Interés estimado 1-10")


class TrendReport(Strict):
    summary: str
    items: list[TrendItem]


class VideoIdea(Strict):
    working_title: str
    angle: str = Field(description="Ángulo único que diferencia el vídeo")
    hook: str = Field(description="Primera frase (0-3 s) que retiene al espectador")
    pillar: str
    target_format: Literal["short", "long"]
    why_it_will_perform: str
    facts_to_verify: list[str]


class IdeaSlate(Strict):
    ideas: list[VideoIdea]
    chosen_index: int


class Scene(Strict):
    index: int
    narration: str = Field(description="Texto exacto de la voz en off")
    on_screen_text: str = Field(description="Texto corto en pantalla (máx 6 palabras)")
    visual_description: str = Field(description="Qué se ve en pantalla")
    footage_keywords: list[str] = Field(description="Palabras clave para buscar gameplay propio")
    ai_video_prompt: str = Field(description="Prompt en inglés para un generador de vídeo IA")
    camera: str


class Script(Strict):
    title: str
    hook: str
    scenes: list[Scene]
    call_to_action: str
    sources_note: str


class ThumbnailPlan(Strict):
    headline: str = Field(description="2-4 palabras en mayúsculas")
    image_prompt: str = Field(description="Prompt en inglés para la imagen de fondo")
    color_accent: str = Field(description="Color hex, p.ej. #FF2D95")


class SeoPackage(Strict):
    title: str = Field(description="Máx 70 caracteres")
    description: str
    tags: list[str]
    hashtags: list[str]
    chapters: list[str]
    thumbnail: ThumbnailPlan


class ComplianceIssue(Strict):
    severity: Literal["block", "warn"]
    area: str
    detail: str
    fix: str


class ComplianceReport(Strict):
    approved: bool
    synthetic_media_disclosure_needed: bool
    issues: list[ComplianceIssue]
