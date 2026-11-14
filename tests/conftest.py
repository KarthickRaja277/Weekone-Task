import json
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.storage import DATA_FILE


@pytest.fixture
def client(tmp_path, monkeypatch):
    data_file = tmp_path / "employees.json"
    data_file.write_text(
        json.dumps([{"name": "Ravi", "salary": 50000}]), encoding="utf-8"
    )
    monkeypatch.setattr("src.main.load_employees", lambda: json.loads(data_file.read_text()))
    monkeypatch.setattr("src.main.save_employees", lambda rows: data_file.write_text(json.dumps(rows)))
    return TestClient(app)
