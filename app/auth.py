from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flasgger import swag_from
from .credentials import USERS

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["POST"])
@swag_from({
    'tags': ['0_Auth'],
    'description': 'Login to get JWT token',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'example': 'admin'},
                    'password': {'type': 'string', 'example': 'admin123'}
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        200: {'description': 'JWT token returned'},
        401: {'description': 'Invalid credentials'}
    }
})
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    if USERS.get(username) == password:
        token = create_access_token(identity=username)
        return jsonify(access_token=token)
    else:
        return jsonify({"msg": "Invalid credentials"}), 401