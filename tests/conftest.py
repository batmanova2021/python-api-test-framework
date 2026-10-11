"""
Global PyTest configuration and fixtures for the API test framework.

Designed to run identically locally and in GitHub Actions:
- Config comes from environment variables (via config.settings) with .env fallback.
- Every request/response is attached to the Allure report for CI debugging.
- Explicit timeouts on every request prevent CI hangs.
"""

import json
import os
from collections.abc import Callable, Iterator
from pathlib import Path

import jsonschema
import pytest

from config.client import ApiClient
from config.settings import Settings, positive_timeout, settings, validate_url


# ============================================================
# CLI Options
# ============================================================
def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--jsonplaceholder-base-url", type=validate_url, default=None)
    parser.addoption("--rick-and-morty-base-url", type=validate_url, default=None)
    parser.addoption("--api-timeout", type=positive_timeout, default=None)


# ============================================================
# Allure Environment Info (shown at the top of the report)
# ============================================================
@pytest.fixture(scope="session", autouse=True)
def allure_environment(request: pytest.FixtureRequest) -> None:
    """Write environment info to allure-results so CI reports show context."""
    results_dir = Path("allure-results")
    results_dir.mkdir(parents=True, exist_ok=True)

    cfg: Settings = request.getfixturevalue("settings_fixture")
    env_info = {
        "JSONPlaceholder.URL": cfg.jsonplaceholder_base_url,
        "RickAndMorty.URL": cfg.rick_and_morty_base_url,
        "Timeout.Seconds": cfg.api_timeout,
        "Python.Version": os.sys.version.split()[0],
        "CI": os.getenv("GITHUB_ACTIONS", "false"),
        "Runner.OS": os.getenv("RUNNER_OS", "local"),
        "Git.Branch": os.getenv("GITHUB_REF_NAME", "local"),
        "Git.SHA": os.getenv("GITHUB_SHA", "local")[:7],
    }

    with (results_dir / "environment.properties").open("w", encoding="utf-8") as f:
        for key, value in env_info.items():
            f.write(f"{key}={value}\n")


# ============================================================
# Settings & API Clients
# ============================================================
@pytest.fixture(scope="session")
def settings_fixture(request: pytest.FixtureRequest) -> Settings:
    return Settings(
        jsonplaceholder_base_url=request.config.getoption("--jsonplaceholder-base-url")
        or settings.jsonplaceholder_base_url,
        rick_and_morty_base_url=request.config.getoption("--rick-and-morty-base-url")
        or settings.rick_and_morty_base_url,
        api_timeout=request.config.getoption("--api-timeout") or settings.api_timeout,
    )


@pytest.fixture(scope="session")
def jsonplaceholder_api(settings_fixture: Settings) -> Iterator[ApiClient]:
    client = ApiClient(settings_fixture.jsonplaceholder_base_url, settings_fixture.api_timeout)
    try:
        yield client
    finally:
        client.close()


@pytest.fixture(scope="session")
def rick_and_morty_api(settings_fixture: Settings) -> Iterator[ApiClient]:
    client = ApiClient(settings_fixture.rick_and_morty_base_url, settings_fixture.api_timeout)
    try:
        yield client
    finally:
        client.close()


# ============================================================
# Schema Validation
# ============================================================
@pytest.fixture(scope="session")
def validate_schema() -> Callable[[object, str], None]:
    def validate(payload: object, filename: str) -> None:
        path = Path(__file__).resolve().parents[1] / "schemas" / filename
        schema = json.loads(path.read_text(encoding="utf-8"))
        jsonschema.validate(payload, schema)

    return validate
