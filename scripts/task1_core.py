from typing import Any


def calculate_bonus(
    salary: float, rate: float = 0.1, *extras: float, **options: Any
) -> float:
    bonus = salary * rate + sum(extras)
    cap = options.get("cap")
    return min(bonus, float(cap)) if cap is not None else bonus


def log_call(func: Any) -> Any:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


class Employee:
    def __init__(self, name: str, salary: float) -> None:
        self.name = name
        self.salary = salary

    def get_details(self) -> str:
        return f"{self.name} - {self.salary}"

    @property
    def annual_salary(self) -> float:
        return self.salary * 12


class Manager(Employee):
    def __init__(self, name: str, salary: float, team_size: int) -> None:
        super().__init__(name, salary)
        self.team_size = team_size

    @log_call
    def get_details(self) -> str:
        return f"{self.name} - {self.salary} - Team Size: {self.team_size}"


def main() -> None:
    import csv
    from pathlib import Path

    with Path("employees.csv").open("r", encoding="utf-8", newline="") as file:
        employees = list(csv.DictReader(file))

    for employee in employees:
        salary = float(employee["salary"])
        if salary < 50000:
            category = "Low"
        elif salary < 70000:
            category = "Medium"
        else:
            category = "High"
        print(f"{employee['name']} - {category} Salary")

    manager = Manager("Divya", 75000, 5)
    print(manager.get_details())


if __name__ == "__main__":
    main()
