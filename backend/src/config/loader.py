# src/config/loader.py
import json
import os
from pydantic import BaseModel

class AppConfig(BaseModel):
    db_url: str | None = None
    env: str = "dev"

def load_config(path: str | None = None) -> AppConfig:
    path = path or os.getenv("SWAB_CONFIG_PATH", "config.json")
    if not os.path.exists(path):
        return AppConfig()
    with open(path, "r", encoding="utf-8") as f:
        return AppConfig(**json.load(f))
