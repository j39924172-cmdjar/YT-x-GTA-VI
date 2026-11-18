"""Estado persistente de cada producción (permite reanudar y auditar)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class RunState:
    def __init__(self, run_dir: Path):
        self.dir = run_dir
        self.dir.mkdir(parents=True, exist_ok=True)
        self.file = run_dir / "state.json"
        self.data: dict[str, Any] = (
            json.loads(self.file.read_text(encoding="utf-8")) if self.file.exists() else {"steps": {}}
        )

    @property
    def run_id(self) -> str:
        return self.dir.name

    def done(self, step: str) -> bool:
        return step in self.data["steps"]

    def get(self, step: str) -> Any:
        return self.data["steps"].get(step)

    def save(self, step: str, value: Any) -> None:
        self.data["steps"][step] = value
        self.data["updated_at"] = datetime.now(timezone.utc).isoformat()
        self.file.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")

    def set_meta(self, **kwargs: Any) -> None:
        self.data.update(kwargs)
        self.file.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")
