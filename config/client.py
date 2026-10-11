import json
from typing import Any

import allure
import requests


class ApiClient:
    """Reusable HTTP session with a timeout and Allure request evidence."""

    def __init__(self, base_url: str, timeout: float) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def get(self, path: str, *, params: dict[str, Any] | None = None) -> requests.Response:
        url = f"{self.base_url}/{path.lstrip('/')}"
        with allure.step(f"GET {url}"):
            allure.attach(
                json.dumps({"url": url, "params": params, "timeout": self.timeout}),
                name="Request",
                attachment_type=allure.attachment_type.JSON,
            )
            response = self.session.get(url, params=params, timeout=self.timeout)
            allure.attach(
                f"Status: {response.status_code}\n{response.text[:5000]}",
                name="Response",
                attachment_type=allure.attachment_type.TEXT,
            )
            return response

    def close(self) -> None:
        self.session.close()
