import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

COINGECKO_API = "https://api.coingecko.com/api/v3"
HEADERS = {"accept": "application/json"}
API_KEY = os.getenv("API_KEY")  # Now it's loaded from .env

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "CoinGecko API Wrapper",
        "description": "API that wraps selected endpoints from CoinGecko and adds authentication",
        "version": "1.0"
    },
    "securityDefinitions": {
        "ApiKeyAuth": {
            "type": "apiKey",
            "name": "x-api-key",
            "in": "header"
        }
    },
    "security": [{"ApiKeyAuth": []}]
}


