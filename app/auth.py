from flask import request, abort
from functools import wraps
from .config import API_KEY

def require_api_key(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        client_key = request.headers.get("x-api-key")
        if client_key and client_key == API_KEY:
            return func(*args, **kwargs)
        abort(401, description="Unauthorized: Missing or invalid API key")
    return decorated
