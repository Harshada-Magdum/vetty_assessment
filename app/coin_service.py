import requests
from .config import HEADERS

def fetch_data_from_api(endpoint):
    try:
        response = requests.get(endpoint, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}, response.status_code
    except requests.exceptions.RequestException as req_err:
        return {"error": f"Request error occurred: {req_err}"}, 500
