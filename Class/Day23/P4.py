# Testing API Endpoints
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from typing import Optional
# ===== API Application =====
app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id < 1:
        return {"error": "Invalid user ID"}

    users = {
        1: {"id": 1, "name": "Alice"},
        2: {"id": 2, "name": "Bob"}
    }

    if user_id in users:
        return users[user_id]

    return {"error": "User not found"}

@app.post("/users")
async def create_user(
    name: Optional[str] = None,
    email: Optional[str] = None
):
    if not name or not email:
        return {"error": "Name and email required"}
    return {"id": 3, "name": name, "email": email}

# ===== API Tests =====
client = TestClient(app)
def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_get_user_exists():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Alice"}

def test_get_user_not_exists():
    response = client.get("/users/999")
    assert response.status_code == 200  # We returned 200 with error
    assert response.json() == {"error": "User not found"}

def test_get_user_invalid_id():
    response = client.get("/users/0")
    assert response.status_code == 200
    assert response.json() == {"error": "Invalid user ID"}

def test_create_user():
    response = client.post("/users", params={"name": "Charlie", "email": "charlie@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Charlie"
    assert data["email"] == "charlie@example.com"

def test_create_user_missing_data():
    response = client.post("/users", params={"name": "Charlie"})
    assert response.status_code == 200
    assert response.json() == {"error": "Name and email required"}

# ===== Running Tests =====
# python -m pytest P4.py -v

