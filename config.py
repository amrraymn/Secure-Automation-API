from __future__ import annotations

import os
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else BASE_DIR


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{RUNTIME_DIR / 'automation_egypt_pro.db'}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    SECURITY_API_TOKEN = os.getenv("SECURITY_API_TOKEN", "dev-token-change-me")
    SECURITY_ENFORCE_AUTH = os.getenv("SECURITY_ENFORCE_AUTH", "1") == "1"
    SECURITY_LOG_PATH = os.getenv("SECURITY_LOG_PATH", str(RUNTIME_DIR / "security_logs.txt"))
