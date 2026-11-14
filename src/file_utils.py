import json
import logging
from pathlib import Path
from typing import Any, Optional, Union

logger = logging.getLogger(__name__)


def read_file(path: Union[str, Path]) -> Optional[dict[str, Any]]:
    file_path = Path(path)
    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        logger.error("File not found: %s", file_path)
        return None
    except json.JSONDecodeError as error:
        logger.error("Invalid JSON in %s: %s", file_path, error)
        return None
    if isinstance(data, dict):
        return data
    logger.error("Expected a JSON object in %s", file_path)
    return None


def find_employee(name: str, employees: list[dict[str, Any]]) -> Optional[dict[str, Any]]:
    for employee in employees:
        if str(employee.get("name", "")).casefold() == name.casefold():
            return employee
    return None
