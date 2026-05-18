import json
import os
import sqlite3
from pathlib import Path
from typing import Any


DEFAULT_BASE_URL = "https://api.venice.ai/api/v1"
DEFAULT_USER_ID = "local_user"


def dejavu_dir() -> Path:
    return Path(os.environ.get("DEJAVU_DIR", "~/.dejavu")).expanduser()


def config_path() -> Path:
    return Path(os.environ.get("DEJAVU_CONFIG", dejavu_dir() / "config.json")).expanduser()


def memory_db_path() -> Path:
    return Path(os.environ.get("DEJAVU_MEMORY_DB", dejavu_dir() / "memories.db")).expanduser()


def default_config() -> dict[str, Any]:
    return {
        "llm": {
            "provider": os.environ.get("DEJAVU_LLM_PROVIDER", "venice"),
            "config": {
                "model": os.environ.get("DEJAVU_LLM_MODEL", "default"),
                "base_url": DEFAULT_BASE_URL,
                "api_key": os.environ.get("VENICE_API_KEY"),
                "temperature": 0.0,
            },
        },
        "embedder": {
            "provider": os.environ.get("DEJAVU_EMBEDDER_PROVIDER", "openai"),
            "config": {},
        },
        "storage": {"history_db_path": str(memory_db_path())},
        "history_db_path": str(memory_db_path()),
        "privacy": {"telemetry": False, "cloud_sync": False},
    }


def ensure_local_files() -> None:
    dejavu_dir().mkdir(parents=True, exist_ok=True)
    memory_db_path().parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(memory_db_path()) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                memory TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def write_default_config(force: bool = False) -> Path:
    ensure_local_files()
    path = config_path()
    if force or not path.exists():
        cfg = default_config()
        cfg["llm"]["config"].pop("api_key", None)
        path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    return path


def load_dejavu_config() -> dict[str, Any]:
    ensure_local_files()
    path = config_path()
    if not path.exists():
        write_default_config()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        data = {}
    cfg = default_config()
    cfg.update(data if isinstance(data, dict) else {})
    cfg["history_db_path"] = cfg.get("history_db_path") or cfg.get("storage", {}).get("history_db_path") or str(memory_db_path())
    return cfg
