from __future__ import annotations

import json
import os
import sys
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

    @classmethod
    def _user_settings_path(cls) -> Path:
        """Return the user-writable settings path (used for saving in frozen builds)."""
        base = Path(os.path.expanduser("~")) / ".ShadowFight2EasySwitch"
        return base / "settings.json"

    @classmethod
    def _default_settings_path(cls) -> Path:
        """Return the built-in default settings path inside the project or bundle."""
        return Path(get_dir("config/settings.json"))

    @classmethod
    def instance(cls) -> "AppSettings":
        """Return the singleton AppSettings instance, creating it on first use."""
        if cls._instance is None:
            cls._instance = cls.load()
        return cls._instance

    @classmethod
    def load(cls) -> "AppSettings":
        """Load settings from JSON file, preferring user settings in frozen builds."""
        try:
            if getattr(sys, "frozen", False):
                user_path = cls._user_settings_path()
                if user_path.exists():
                    with user_path.open("r", encoding="utf-8") as f:
                        data = json.load(f)
                    return cls(
                        export_dir_model=data.get("export_dir_model", "./model"),
                        export_dir_animation=data.get("export_dir_animation", "./animation"),
                        language=data.get("language", "en"),
                    )

                default_path = cls._default_settings_path()
                if default_path.exists():
                    with default_path.open("r", encoding="utf-8") as f:
                        data = json.load(f)
                    return cls(
                        export_dir_model=data.get("export_dir_model", "./model"),
                        export_dir_animation=data.get("export_dir_animation", "./animation"),
                        language=data.get("language", "en"),
                    )

            # Non-frozen (dev) mode: use project config/settings.json
            path = cls._default_settings_path()
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
        try:
            if getattr(sys, "frozen", False):
                path = self._user_settings_path()
            else:
                path = self._default_settings_path()

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

