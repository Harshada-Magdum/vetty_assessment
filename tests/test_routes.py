import pytest
from unittest.mock import patch
from flask.testing import FlaskClient
from app.auth import require_api_key
from run import app  # Update this import path to your app entry

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

# --------------------------
# Test /coins/all endpoint
# --------------------------

@patch("app.routes.fetch_data_from_api")
@patch("app.routes.require_api_key", new=lambda f: f)  # bypass @require_api_key
def test_list_all_coins_unit_success(mock_fetch, client: FlaskClient):
    mock_data = [
        {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"},
        {"id": "ethereum", "symbol": "eth", "name": "Ethereum"}
    ]
    mock_fetch.return_value = mock_data

    response = client.get("/coins/all?page_num=1&per_page=1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["total_coins"] == 2
    assert data["page_num"] == 1
    assert data["per_page"] == 1
    assert len(data["coins"]) == 1
    assert data["coins"][0]["id"] == "bitcoin"

@patch("app.routes.fetch_data_from_api", side_effect=Exception("API failure"))
@patch("app.routes.require_api_key", lambda f: f)
def test_list_all_coins_unit_failure(mock_fetch, client: FlaskClient):
    response = client.get("/coins/all")
    assert response.status_code == 500
    data = response.get_json()
    assert "error" in data

# --------------------------
# Test /categories endpoint
# --------------------------

@patch("app.routes.fetch_data_from_api")
@patch("app.routes.require_api_key", lambda f: f)
def test_list_categories_unit_success(mock_fetch, client: FlaskClient):
    mock_data = [
        {"category_id": "defi", "name": "DeFi"},
        {"category_id": "stablecoins", "name": "Stablecoins"}
    ]
    mock_fetch.return_value = mock_data

    response = client.get("/categories?page_num=1&per_page=1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["total_categories"] == 2
    assert data["page_num"] == 1
    assert data["per_page"] == 1
    assert len(data["categories"]) == 1
    assert data["categories"][0]["category_id"] == "defi"

@patch("app.routes.fetch_data_from_api", side_effect=Exception("API failure"))
@patch("app.routes.require_api_key", lambda f: f)
def test_list_categories_unit_failure(mock_fetch, client: FlaskClient):
    response = client.get("/categories")
    assert response.status_code == 500
    data = response.get_json()
    assert "error" in data

# --------------------------
# Test /coin/<coin_id> endpoint
# --------------------------

@patch("app.routes.fetch_data_from_api")
@patch("app.routes.require_api_key", lambda f: f)
def test_get_coin_data_unit_success(mock_fetch, client: FlaskClient):
    mock_fetch.return_value = {
        "id": "bitcoin",
        "symbol": "btc",
        "name": "Bitcoin"
    }

    response = client.get("/coin/bitcoin")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == "bitcoin"
    assert data["symbol"] == "btc"

@patch("app.routes.fetch_data_from_api", side_effect=Exception("Coin not found"))
@patch("app.routes.require_api_key", lambda f: f)
def test_get_coin_data_unit_failure(mock_fetch, client: FlaskClient):
    response = client.get("/coin/nonexistent")
    assert response.status_code == 500 or response.status_code == 404
    data = response.get_json()
    assert "error" in data
