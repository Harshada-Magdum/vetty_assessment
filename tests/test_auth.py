import json
from app.credentials import USERS

def test_successful_login(client):
    response = client.post("/login", json={
        "username": "admin",  # You can replace with any valid username
        "password": "admin123"  # Use the corresponding password
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data

def test_failed_login(client):
    response = client.post("/login", json={
        "username": "wronguser",  # Invalid username
        "password": "wrongpass"  # Invalid password
    })
    assert response.status_code == 401
    assert response.get_json()["msg"] == "Invalid credentials"