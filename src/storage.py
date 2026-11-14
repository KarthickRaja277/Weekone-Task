import json
from pathlib import Path
from typing import Any

DATA_FILE = Path(__file__).resolve().parents[1] / "employees.json"


def load_employees(path: Path = DATA_FILE) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError("employees.json must contain a JSON list")
    return data


def save_employees(employees: list[dict[str, Any]], path: Path = DATA_FILE) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(employees, file, indent=2)
