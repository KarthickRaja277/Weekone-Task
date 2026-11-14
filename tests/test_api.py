def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_employees(client):
    response = client.get("/employees")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Ravi"


def test_get_employee_success(client):
    response = client.get("/employees/Ravi")
    assert response.status_code == 200
    assert response.json()["salary"] == 50000


def test_get_employee_not_found(client):
    response = client.get("/employees/Unknown")
    assert response.status_code == 404


def test_create_employee_success(client):
    response = client.post("/employees", json={"name": "Maya", "salary": 42000})
    assert response.status_code == 201
    assert response.json()["name"] == "Maya"


def test_invalid_salary(client):
    response = client.post("/employees", json={"name": "Maya", "salary": -5})
    assert response.status_code == 422


def test_empty_name(client):
    response = client.post("/employees", json={"name": "   ", "salary": 100})
    assert response.status_code == 422
