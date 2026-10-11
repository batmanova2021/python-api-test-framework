from unittest.mock import Mock

import pytest
import requests

from config.client import ApiClient
from config.settings import Settings, positive_timeout, validate_url

pytestmark = pytest.mark.unit


@pytest.mark.parametrize("value", ["0", "-1", "nan", "inf", "invalid"])
def test_reject_invalid_timeout(value):
    with pytest.raises(ValueError, match=r"API_TIMEOUT|could not convert"):
        positive_timeout(value)


def test_environment_settings(monkeypatch):
    monkeypatch.setenv("JSONPLACEHOLDER_BASE_URL", "https://example.com/posts/")
    monkeypatch.setenv("RICK_AND_MORTY_BASE_URL", "https://example.com/api/")
    monkeypatch.setenv("API_TIMEOUT", "2.5")
    s = Settings.from_env()
    assert s.jsonplaceholder_base_url == "https://example.com/posts"
    assert s.rick_and_morty_base_url == "https://example.com/api"
    assert s.api_timeout == 2.5


@pytest.mark.parametrize("url", ["example.com", "ftp://example.com", "https://"])
def test_reject_invalid_base_url(url):
    with pytest.raises(ValueError, match="API base URLs must be absolute"):
        validate_url(url)


def test_client_builds_url_and_passes_timeout(monkeypatch):
    response = requests.Response()
    response.status_code = 200
    response._content = b'{"id": 1}'  # pylint: disable=protected-access
    get = Mock(return_value=response)
    close = Mock()
    client = ApiClient("https://example.com/api", 2.5)
    monkeypatch.setattr(client.session, "get", get)
    monkeypatch.setattr(client.session, "close", close)
    try:
        assert client.get("/character", params={"name": "Rick"}) is response
        get.assert_called_once_with(
            "https://example.com/api/character", params={"name": "Rick"}, timeout=2.5
        )
    finally:
        client.close()
    close.assert_called_once_with()
