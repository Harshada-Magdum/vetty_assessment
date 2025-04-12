from flask import Flask, request, jsonify
import requests
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger = Swagger(app)

COINGECKO_API = "https://api.coingecko.com/api/v3"
HEADERS = {"accept": "application/json"}

def paginate_list(data, page_num=1, per_page=10):
    """Helper function to paginate a list."""
    start = (page_num - 1) * per_page
    end = start + per_page
    return data[start:end]

def fetch_data_from_api(endpoint):
    """Helper function to fetch data from the CoinGecko API."""
    try:
        response = requests.get(endpoint, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}, response.status_code
    except requests.exceptions.RequestException as req_err:
        return {"error": f"Request error occurred: {req_err}"}, 500

@app.route("/coins/all", methods=["GET"])
@swag_from({
    'tags': ['1_Coins'],
    'parameters': [
        {
            'name': 'page_num',
            'in': 'query',
            'type': 'integer',
            'default': 1,
            'required': False
        },
        {
            'name': 'per_page',
            'in': 'query',
            'type': 'integer',
            'default': 10,
            'required': False
        }
    ],
    'responses': {200: {'description': 'Paginated list of coins'}}
})
def list_all_coins():
    """Endpoint to list all coins with pagination."""
    url = f"{COINGECKO_API}/coins/list"
    data = fetch_data_from_api(url)

    if isinstance(data, tuple):  # Error occurred
        return jsonify(data[0]), data[1]

    page_num = int(request.args.get("page_num", 1))
    per_page = int(request.args.get("per_page", 10))
    paginated = paginate_list(data, page_num, per_page)

    return jsonify({
        "total_coins": len(data),
        "page_num": page_num,
        "per_page": per_page,
        "coins": paginated
    })

@app.route("/categories", methods=["GET"])
@swag_from({
    'tags': ['2_Categories'],
    'parameters': [
        {
            'name': 'page_num',
            'in': 'query',
            'type': 'integer',
            'default': 1,
            'required': False
        },
        {
            'name': 'per_page',
            'in': 'query',
            'type': 'integer',
            'default': 10,
            'required': False
        }
    ],
    'responses': {200: {'description': 'Paginated list of categories'}}
})
def list_categories():
    """Endpoint to list all categories with pagination."""
    url = f"{COINGECKO_API}/coins/categories/list"
    data = fetch_data_from_api(url)

    if isinstance(data, tuple):  # Error occurred
        return jsonify(data[0]), data[1]

    page_num = int(request.args.get("page_num", 1))
    per_page = int(request.args.get("per_page", 10))
    paginated = paginate_list(data, page_num, per_page)

    return jsonify({
        "total_categories": len(data),
        "page_num": page_num,
        "per_page": per_page,
        "categories": paginated
    })

@app.route("/coin/<coin_id>", methods=["GET"])
@swag_from({
    'tags': ['3_Coin Details'],
    'parameters': [
        {
            'name': 'coin_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID of the coin (e.g., bitcoin, ethereum)'
        }
    ],
    'responses': {
        200: {'description': 'Detailed coin data'},
        404: {'description': 'Coin not found'}
    }
})
def get_coin_data(coin_id):
    """Endpoint to get detailed data of a specific coin."""
    url = f"{COINGECKO_API}/coins/{coin_id}"
    data = fetch_data_from_api(url)

    if isinstance(data, tuple):  # Error occurred
        return jsonify(data[0]), data[1]

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)