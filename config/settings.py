"""
Central configuration for the API test framework.

Loads settings from environment variables with sensible defaults.
Local development reads from .env; CI reads from GitHub Actions variables.
"""

import math
import os
from dataclasses import dataclass
from urllib.parse import urlsplit

from dotenv import load_dotenv

# Load .env for local development. In CI, env vars are already set.
load_dotenv()


def positive_timeout(value: str) -> float:
    timeout = float(value)
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("API_TIMEOUT must be a finite number greater than zero")
    return timeout


def validate_url(value: str) -> str:
    url = value.rstrip("/")
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("API base URLs must be absolute HTTP or HTTPS URLs")
    return url


@dataclass(frozen=True)
class Settings:
    """Immutable settings loaded from environment variables."""

    jsonplaceholder_base_url: str
    rick_and_morty_base_url: str
    api_timeout: float

    @classmethod
    def from_env(cls) -> Settings:
        load_dotenv()
        return cls(
            jsonplaceholder_base_url=validate_url(
                os.getenv("JSONPLACEHOLDER_BASE_URL", "https://jsonplaceholder.typicode.com")
            ),
            rick_and_morty_base_url=validate_url(
                os.getenv("RICK_AND_MORTY_BASE_URL", "https://rickandmortyapi.com/api")
            ),
            api_timeout=positive_timeout(os.getenv("API_TIMEOUT", "10")),
        )


# Module-level singleton — import and use directly in conftest and fixtures.
settings = Settings.from_env()
