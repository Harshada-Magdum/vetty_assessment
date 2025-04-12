import pytest
from flask import Flask
from flask.testing import FlaskClient
from main import app  # Import the Flask app
import requests_mock

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_list_all_coins_success(client: FlaskClient):
    with requests_mock.Mocker() as mocker:
        mocker.get(
            "https://api.coingecko.com/api/v3/coins/list",
            json=[{"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"}]
        )
        response = client.get("/coins/all?page_num=1&per_page=1")
        assert response.status_code == 200
        data = response.get_json()
        assert data["total_coins"] == 1
        assert data["page_num"] == 1
        assert data["per_page"] == 1
        assert data["coins"] == [{"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"}]

def test_list_all_coins_failure(client: FlaskClient):
    with requests_mock.Mocker() as mocker:
        mocker.get(
            "https://api.coingecko.com/api/v3/coins/list",
            status_code=500
        )
        response = client.get("/coins/all")
        assert response.status_code == 500
        data = response.get_json()
        assert data["error"] == "Failed to fetch data from CoinGecko"

def test_list_categories_success(client: FlaskClient):
    with requests_mock.Mocker() as mocker:
        mocker.get(
            "https://api.coingecko.com/api/v3/coins/categories/list",
            json=[{"id": "defi", "name": "DeFi"}]
        )
        response = client.get("/categories?page_num=1&per_page=1")
        assert response.status_code == 200
        data = response.get_json()
        assert data["total_categories"] == 1
        assert data["page_num"] == 1
        assert data["per_page"] == 1
        assert data["categories"] == [{"id": "defi", "name": "DeFi"}]

def test_list_categories_failure(client: FlaskClient):
    with requests_mock.Mocker() as mocker:
        mocker.get(
            "https://api.coingecko.com/api/v3/coins/categories/list",
            status_code=500
        )
        response = client.get("/categories")
        assert response.status_code == 500
        data = response.get_json()
        assert data["error"] == "Failed to fetch categories from CoinGecko"

def test_get_coin_data_success(client: FlaskClient):
    with requests_mock.Mocker() as mocker:
        mocker.get(
            "https://api.coingecko.com/api/v3/coins/bitcoin",
            json={"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"}
        )
        response = client.get("/coin/bitcoin")
        assert response.status_code == 200
        data = response.get_json()
        assert data["id"] == "bitcoin"
        assert data["symbol"] == "btc"
        assert data["name"] == "Bitcoin"

def test_get_coin_data_not_found(client: FlaskClient):
    with requests_mock.Mocker() as mocker:
        mocker.get(
            "https://api.coingecko.com/api/v3/coins/nonexistent",
            status_code=404
        )
        response = client.get("/coin/nonexistent")
        assert response.status_code == 404
        data = response.get_json()
        assert data["error"] == "Coin 'nonexistent' not found"

def test_get_coin_data_failure(client: FlaskClient):
    with requests_mock.Mocker() as mocker:
        mocker.get(
            "https://api.coingecko.com/api/v3/coins/bitcoin",
            status_code=500
        )
        response = client.get("/coin/bitcoin")
        assert response.status_code == 500
        data = response.get_json()
        assert data["error"] == "Failed to fetch coin data"
