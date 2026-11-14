import csv
import json
import logging
import sys
from pathlib import Path
from typing import Any, Optional, Union

import fitz
from openpyxl import Workbook, load_workbook

from src.file_utils import find_employee, read_file

logger = logging.getLogger(__name__)


def read_employees(path: Union[str, Path]) -> list[dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8", newline="") as file:
        return [
            {**row, "salary": int(row["salary"])}
            for row in csv.DictReader(file)
        ]


def write_json(employees: list[dict[str, Any]], path: Union[str, Path]) -> None:
    with Path(path).open("w", encoding="utf-8") as file:
        json.dump(employees, file, indent=2)


def write_high_earners(
    employees: list[dict[str, Any]], path: Union[str, Path]
) -> int:
    high_earners = [employee for employee in employees if employee["salary"] > 50000]
    with Path(path).open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "department", "salary"])
        writer.writeheader()
        writer.writerows(high_earners)
    return len(high_earners)


def create_and_read_excel(
    employees: list[dict[str, Any]], path: Union[str, Path]
) -> int:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Salaries"
    sheet.append(["name", "department", "salary"])
    for employee in employees:
        sheet.append(
            [employee["name"], employee["department"], employee["salary"]]
        )
    workbook.save(path)
    loaded = load_workbook(path, read_only=True, data_only=True)
    row_count = max(loaded.active.max_row - 1, 0)
    loaded.close()
    return row_count


def extract_first_page(path: Union[str, Path]) -> str:
    with fitz.open(path) as document:
        if not document:
            return ""
        return document[0].get_text()[:100]


def main() -> None:
    logging.basicConfig(level=logging.ERROR, format="%(levelname)s - %(message)s")
    base = Path(__file__).resolve().parents[1]
    employees = read_employees(base / "employees.csv")
    write_json(employees, base / "employees.json")
    high_count = write_high_earners(employees, base / "high_earners.csv")
    excel_count = create_and_read_excel(employees, base / "salary.xlsx")
    print(f"Rows read: {len(employees)} | High earners written: {high_count}")
    print(f"salary.xlsx created and read back: {excel_count} rows")
    read_file(base / "missing.txt")
    if len(sys.argv) > 1:
        print(extract_first_page(sys.argv[1]))
    print(f"Find Arun: {find_employee('Arun', employees)}")


if __name__ == "__main__":
    main()
