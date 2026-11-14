import os
from typing import Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_session() -> requests.Session:
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=frozenset(["GET"]),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    api_key = os.getenv("API_KEY")
    if api_key:
        session.headers.update({"X-API-Key": api_key})
    return session


def fetch_users() -> list[dict[str, Any]]:
    response = create_session().get(
        "https://jsonplaceholder.typicode.com/users", timeout=15
    )
    response.raise_for_status()
    payload: Any = response.json()
    if not isinstance(payload, list):
        raise ValueError("Expected a list of users")
    return payload
