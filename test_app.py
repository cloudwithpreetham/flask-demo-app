import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["message"] == "Welcome to the Flask Demo App!"

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "OK"

def test_echo_valid(client):
    response = client.post("/api/echo", json={"message": "DevOps Task 2"})
    assert response.status_code == 201
    assert response.json["echo"] == "DevOps Task 2"

def test_echo_invalid(client):
    response = client.post("/api/echo", json={})
    assert response.status_code == 400
    assert "error" in response.json
