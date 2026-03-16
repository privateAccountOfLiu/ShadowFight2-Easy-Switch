from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from python.core.core_functions import get_dir, write_to_log


@dataclass
class AppSettings:
    """Application-wide settings for export directories and language preference."""

    export_dir_model: str = "./model"
    export_dir_animation: str = "./animation"
    language: str = "en"

    _instance: ClassVar["AppSettings | None"] = None
    _settings_path: ClassVar[Path] = Path(get_dir("config/settings.json"))

    @classmethod
    def instance(cls) -> "AppSettings":
        """Return the singleton AppSettings instance, creating it on first use."""
        if cls._instance is None:
            cls._instance = cls.load()
        return cls._instance

    @classmethod
    def load(cls) -> "AppSettings":
        """Load settings from JSON file, falling back to defaults if not present."""
        path = cls._settings_path
        try:
            if path.exists():
                with path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                return cls(
                    export_dir_model=data.get("export_dir_model", "./model"),
                    export_dir_animation=data.get("export_dir_animation", "./animation"),
                    language=data.get("language", "en"),
                )
        except Exception as e:
            write_to_log(f"[Settings] failed to load: {e}")
        return cls()

    def save(self) -> None:
        """Persist settings to JSON file."""
        path = self._settings_path
        try:
            os.makedirs(path.parent, exist_ok=True)
            with path.open("w", encoding="utf-8") as f:
                json.dump(
                    {
                        "export_dir_model": self.export_dir_model,
                        "export_dir_animation": self.export_dir_animation,
                        "language": self.language,
                    },
                    f,
                    ensure_ascii=False,
                    indent=2,
                )
        except Exception as e:
            write_to_log(f"[Settings] failed to save: {e}")

