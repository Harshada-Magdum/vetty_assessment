from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from .service import fetch_data_from_api
from .utils import paginate_list
from .config import COINGECKO_API

routes_bp = Blueprint('routes', __name__)

@routes_bp.route("/coins/all", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['1_Coins'],
    'parameters': [
        {'name': 'page_num', 'in': 'query', 'type': 'integer', 'default': 1},
        {'name': 'per_page', 'in': 'query', 'type': 'integer', 'default': 10}
    ],
    'security': [{"Bearer": []}],
    'responses': {200: {'description': 'Paginated list of coins'}}
})
def list_all_coins():
    url = f"{COINGECKO_API}/coins/list"
    data = fetch_data_from_api(url)
    if isinstance(data, tuple): return jsonify(data[0]), data[1]
    page_num = int(request.args.get("page_num", 1))
    per_page = int(request.args.get("per_page", 10))
    return jsonify({
        "total_coins": len(data),
        "page_num": page_num,
        "per_page": per_page,
        "coins": paginate_list(data, page_num, per_page)
    })

@routes_bp.route("/categories", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['2_Categories'],
    'parameters': [
        {'name': 'page_num', 'in': 'query', 'type': 'integer', 'default': 1},
        {'name': 'per_page', 'in': 'query', 'type': 'integer', 'default': 10}
    ],
    'security': [{"Bearer": []}],
    'responses': {200: {'description': 'Paginated list of categories'}}
})
def list_categories():
    url = f"{COINGECKO_API}/coins/categories/list"
    data = fetch_data_from_api(url)
    if isinstance(data, tuple): return jsonify(data[0]), data[1]
    page_num = int(request.args.get("page_num", 1))
    per_page = int(request.args.get("per_page", 10))
    return jsonify({
        "total_categories": len(data),
        "page_num": page_num,
        "per_page": per_page,
        "categories": paginate_list(data, page_num, per_page)
    })

@routes_bp.route("/coin/<coin_id>", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['3_Coin Details'],
    'parameters': [
        {'name': 'coin_id', 'in': 'path', 'type': 'string', 'required': True}
    ],
    'security': [{"Bearer": []}],
    'responses': {
        200: {'description': 'Detailed coin data'},
        404: {'description': 'Coin not found'}
    }
})
def get_coin_data(coin_id):
    url = f"{COINGECKO_API}/coins/{coin_id}"
    data = fetch_data_from_api(url)
    if isinstance(data, tuple): return jsonify(data[0]), data[1]
    return jsonify(data)