"""Configuración de la aplicación leída desde variables de entorno."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

DEFAULT_PASSWORD_NOTE = "cambiar-esta-clave"


def _resolve_path(env_name: str, default: str) -> Path:
    raw = os.getenv(env_name, default)
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


class Settings:
    def __init__(self) -> None:
        self.password: str = os.getenv("TECHDEV_PASSWORD", "").strip()
        self.default_password_in_use: bool = self.password == DEFAULT_PASSWORD_NOTE
        raw_secret = os.getenv("TECHDEV_SESSION_SECRET", "").strip()
        self.session_secret: str = raw_secret or hashlib.sha256(
            f"techdev-session::{self.password or 'sin-clave'}".encode("utf-8")
        ).hexdigest()
        self.db_path: Path = _resolve_path("TECHDEV_DB_PATH", "data/app.db")
        self.upload_dir: Path = _resolve_path("TECHDEV_UPLOAD_DIR", "data/uploads")
        self.base_url: str = os.getenv("APP_BASE_URL", "http://localhost:8000").rstrip("/")
        self.session_hours: int = int(os.getenv("TECHDEV_SESSION_HOURS", "12"))
        self.default_lang: str = "es"
        self.languages: tuple[str, ...] = ("es", "en")
        self.max_upload_mb: int = 5

    @property
    def admin_ready(self) -> bool:
        return bool(self.password)

    def ensure_dirs(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.upload_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
