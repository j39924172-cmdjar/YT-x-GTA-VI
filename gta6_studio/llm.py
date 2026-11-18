"""Conexión con Claude: el "cerebro" que comparten los agentes creativos."""

from __future__ import annotations

import json
import logging
from typing import Callable, TypeVar

import anthropic
from pydantic import BaseModel

from .config import Settings

log = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)

FALLBACK_BETA = "server-side-fallback-2026-07-01"


class LLMError(RuntimeError):
    pass


class Brain:
    def __init__(self, settings: Settings):
        self.settings = settings
        cfg = settings["claude"]
        self.model: str = cfg["model"]
        self.effort: str = cfg.get("effort", "high")
        self.use_fallbacks: bool = cfg.get("use_fallbacks", True)
        self.client = None if settings.dry_run else anthropic.Anthropic()

    # ------------------------------------------------------------------ helpers
    def _create(self, **kwargs):
        kwargs.setdefault("model", self.model)
        kwargs.setdefault("output_config", {}).setdefault("effort", self.effort)
        if self.use_fallbacks:
            kwargs["betas"] = [FALLBACK_BETA]
            kwargs["fallbacks"] = "default"
        try:
            with self.client.beta.messages.stream(**kwargs) as stream:
                msg = stream.get_final_message()
        except anthropic.RateLimitError as e:
            raise LLMError(f"Límite de uso de Claude alcanzado: {e.message}") from e
        except anthropic.AuthenticationError as e:
            raise LLMError("ANTHROPIC_API_KEY inválida o ausente") from e
        except anthropic.APIStatusError as e:
            raise LLMError(f"Error de la API de Claude ({e.status_code}): {e.message}") from e
        except anthropic.APIConnectionError as e:
            raise LLMError("No se pudo conectar con la API de Claude") from e
        if msg.stop_reason == "refusal":
            detail = msg.stop_details.explanation if msg.stop_details else ""
            raise LLMError(f"Claude rechazó la petición: {detail}")
        if msg.stop_reason == "max_tokens":
            raise LLMError("Respuesta truncada (max_tokens)")
        return msg

    @staticmethod
    def _text(msg) -> str:
        return "".join(b.text for b in msg.content if b.type == "text")

    # ------------------------------------------------------------------ API
    def structured(
        self,
        system: str,
        prompt: str,
        schema: type[T],
        mock: Callable[[], T],
    ) -> T:
        """Pide a Claude una respuesta validada contra un esquema Pydantic."""
        if self.settings.dry_run:
            return mock()
        msg = self._create(
            max_tokens=32000,
            system=system,
            messages=[{"role": "user", "content": prompt}],
            output_config={
                "format": {"type": "json_schema", "schema": schema.model_json_schema()}
            },
        )
        return schema.model_validate(json.loads(self._text(msg)))

    def research(self, system: str, prompt: str, mock: Callable[[], str], max_searches: int = 8) -> str:
        """Investigación con búsqueda web en vivo (herramienta de servidor de Claude)."""
        if self.settings.dry_run:
            return mock()
        messages = [{"role": "user", "content": prompt}]
        tools = [{"type": "web_search_20260209", "name": "web_search", "max_uses": max_searches}]
        for _ in range(5):  # reanudar si el servidor pausa el turno
            msg = self._create(max_tokens=32000, system=system, messages=messages, tools=tools)
            if msg.stop_reason != "pause_turn":
                return self._text(msg)
            messages.append({"role": "assistant", "content": msg.content})
        return self._text(msg)
