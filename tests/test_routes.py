import json
from app.credentials import USERS
import pytest
from unittest.mock import patch

def get_auth_token(client, username, password):
    """Helper function to obtain JWT token by providing valid credentials"""
    response = client.post("/login", json={
        "username": username,
        "password": password
    })
    return response.get_json()["access_token"]

@pytest.fixture
def mock_get_coin_data():
    """Fixture to mock the CoinGecko API response"""
    with patch("requests.get") as mock_get:
        # Mock the API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"id": "bitcoin", "name": "Bitcoin"}]
        yield mock_get

def test_list_all_coins(client, mock_get_coin_data):
    token = get_auth_token(client, "admin", "admin123")
    response = client.get("/coins/all?page_num=1&per_page=5", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "coins" in data
    assert isinstance(data["coins"], list)

def test_list_categories(client, mock_get_coin_data):
    token = get_auth_token(client, "admin", "admin123")
    response = client.get("/categories", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert "categories" in response.get_json()

def test_get_coin_data_valid(client, mock_get_coin_data):
    token = get_auth_token(client, "admin", "admin123")
    response = client.get("/coin/bitcoin", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    data = response.get_json()
    # Now access the first item in the list and check the 'id' key
    assert data[0]["id"] == "bitcoin"