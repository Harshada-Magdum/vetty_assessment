from flask import Blueprint, request, jsonify
from flasgger import swag_from
from .auth import require_api_key
from .coin_service import fetch_data_from_api
from .utils import paginate_list
from .config import COINGECKO_API

bp = Blueprint("main", __name__)

@bp.route("/coins/all", methods=["GET"])
@require_api_key
@swag_from({
    'tags': ['Coins'],
    'summary': 'List all coins',
    'description': 'Returns a list of all coins from the CoinGecko API, paginated',
    'parameters': [
        {
            'name': 'page_num',
            'in': 'query',
            'type': 'integer',
            'description': 'Page number for pagination',
            'required': False,
            'default': 1
        },
        {
            'name': 'per_page',
            'in': 'query',
            'type': 'integer',
            'description': 'Number of items per page',
            'required': False,
            'default': 10
        }
    ],
    'responses': {
        200: {
            'description': 'A paginated list of coins',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'string'},
                        'symbol': {'type': 'string'},
                        'name': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def list_all_coins():
    page_num = request.args.get('page_num', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    
    data = fetch_data_from_api(f"{COINGECKO_API}/coins/list")
    paginated_data = paginate_list(data, page_num, per_page)
    
    return jsonify(paginated_data)

@bp.route("/categories", methods=["GET"])
@require_api_key
@swag_from({
    'tags': ['Coins'],
    'summary': 'List all categories',
    'description': 'Returns all coin categories from the CoinGecko API, paginated',
    'parameters': [
        {
            'name': 'page_num',
            'in': 'query',
            'type': 'integer',
            'description': 'Page number for pagination',
            'required': False,
            'default': 1
        },
        {
            'name': 'per_page',
            'in': 'query',
            'type': 'integer',
            'description': 'Number of items per page',
            'required': False,
            'default': 10
        }
    ],
    'responses': {
        200: {
            'description': 'Paginated list of categories',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'category_id': {'type': 'string'},
                        'name': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def list_categories():

    page_num = request.args.get('page_num', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    data = fetch_data_from_api(f"{COINGECKO_API}/coins/categories/list")
    paginated_data = paginate_list(data, page_num, per_page)
    return jsonify(paginated_data)
    
    

@bp.route("/coin/<coin_id>", methods=["GET"])
@require_api_key
@swag_from({
    'tags': ['Coins'],
    'summary': 'Get coin data by ID',
    'description': 'Returns market data for a specific coin',
    'parameters': [
        {
            'name': 'coin_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The CoinGecko ID of the coin(e.g., bitcoin, ethereum)'
        }
    ],
    'responses': {
        200: {
            'description': 'Market data for a coin',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'string'},
                    'symbol': {'type': 'string'},
                    'name': {'type': 'string'},
                    'market_data': {'type': 'object'}
                }
            }
        }
    }
})
def get_coin_data(coin_id):
    data = fetch_data_from_api(f"{COINGECKO_API}/coins/{coin_id}")
    return jsonify(data)
