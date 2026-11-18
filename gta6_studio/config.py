"""Carga de configuración (config.yaml + variables de entorno)."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Settings:
    raw: dict[str, Any]
    dry_run: bool = False
    root: Path = field(default=ROOT)

    def __getitem__(self, key: str) -> Any:
        return self.raw[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self.raw.get(key, default)

    @staticmethod
    def env(name: str) -> str | None:
        value = os.environ.get(name)
        return value or None

    @property
    def runs_dir(self) -> Path:
        return self.root / "runs"

    @property
    def data_dir(self) -> Path:
        return self.root / "data"

    def path(self, rel: str) -> Path:
        p = Path(rel)
        return p if p.is_absolute() else self.root / p


def load_settings(config_path: str | None = None, dry_run: bool = False) -> Settings:
    load_dotenv(ROOT / ".env")
    path = Path(config_path) if config_path else ROOT / "config.yaml"
    with open(path, encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)
    return Settings(raw=raw, dry_run=dry_run)
