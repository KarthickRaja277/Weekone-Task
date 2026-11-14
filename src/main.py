from fastapi import FastAPI, HTTPException
from typing import Any

from src.models import EmployeeCreate
from src.storage import load_employees, save_employees

app = FastAPI(title="Weeknd Task", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/employees")
def get_employees() -> list[dict[str, Any]]:
    return load_employees()


@app.get("/employees/{name}")
def get_employee(name: str) -> dict[str, Any]:
    for employee in load_employees():
        if str(employee.get("name", "")).casefold() == name.casefold():
            return employee
    raise HTTPException(status_code=404, detail="Employee not found")


@app.post("/employees", status_code=201)
def create_employee(employee: EmployeeCreate) -> dict[str, Any]:
    employees = load_employees()
    if any(
        str(existing.get("name", "")).casefold() == employee.name.casefold()
        for existing in employees
    ):
        raise HTTPException(status_code=409, detail="Employee already exists")
    new_employee: dict[str, Any] = employee.model_dump()
    employees.append(new_employee)
    save_employees(employees)
    return new_employee
