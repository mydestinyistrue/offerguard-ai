"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings

from dotenv import load_dotenv

load_dotenv()  # reads from .env file automatically

class Settings(BaseSettings):
    """Central configuration – reads .env automatically."""

    # --- API keys ---
    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str
    GROQ_MODEL: str = "openai/gpt-oss-120b"
    VIRUSTOTAL_API_KEY: str = ""

    # --- App settings ---
    ENVIRONMENT: str = "development"
    RATE_LIMIT: int = 30  # requests per minute

    # --- Paths ---
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = (
        (Path(__file__).resolve().parent.parent.parent.parent / "data")
        if (Path(__file__).resolve().parent.parent.parent.parent / "data").exists()
        else (Path(__file__).resolve().parent.parent.parent / "data")
    )

    # --- LLM ---
    GEMINI_MODEL: str = "gemini-2.0-flash"
    LLM_TIMEOUT: int = 30  # seconds
    MAX_INPUT_CHARS: int = 50_000  # hard cap on input text length

    # --- Score blending ---
    RULES_WEIGHT: float = 0.60
    LLM_WEIGHT: float = 0.40

    # --- CORS ---
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()
