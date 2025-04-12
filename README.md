# Flask Server for CoinGecko API Integration

This Flask application provides a RESTful API to interact with the CoinGecko API. It includes endpoints for listing coins, categories, and fetching detailed information about specific coins. The application also supports pagination and integrates Swagger for API documentation.

## Features

- **List all coins** with pagination.
- **List all categories** with pagination.
- **Fetch detailed information** about a specific coin.
- **Swagger integration** for interactive API documentation.

## Requirements

- Python 3.7 or higher
- Flask
- Flasgger
- Requests

## Installation

1. Clone the repository or download the project files:
   ```bash
   git clone <repository-url>
   cd FlaskServer
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask server:
   ```bash
   python flask_server\ 1.py
   ```

5. Access the application at `http://127.0.0.1:5000`.

## API Endpoints

### 1. List All Coins
**Endpoint:** `/coins/all`  
**Method:** `GET`  
**Description:** Returns a paginated list of all coins.  

**Query Parameters:**
- `page_num` (integer, optional): Page number (default: 1).
- `per_page` (integer, optional): Number of items per page (default: 10).

**Response:**
```json
{
  "total_coins": 1234,
  "page_num": 1,
  "per_page": 10,
  "coins": [
    {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"},
    ...
  ]
}
```

---

### 2. List All Categories
**Endpoint:** `/categories`  
**Method:** `GET`  
**Description:** Returns a paginated list of all categories.  

**Query Parameters:**
- `page_num` (integer, optional): Page number (default: 1).
- `per_page` (integer, optional): Number of items per page (default: 10).

**Response:**
```json
{
  "total_categories": 50,
  "page_num": 1,
  "per_page": 10,
  "categories": [
    {"id": "decentralized-finance-defi", "name": "Decentralized Finance (DeFi)"},
    ...
  ]
}
```

---

### 3. Get Coin Details
**Endpoint:** `/coin/<coin_id>`  
**Method:** `GET`  
**Description:** Fetches detailed information about a specific coin.  

**Path Parameters:**
- `coin_id` (string, required): The ID of the coin (e.g., `bitcoin`, `ethereum`).

**Response:**
```json
{
  "id": "bitcoin",
  "symbol": "btc",
  "name": "Bitcoin",
  "market_data": {
    "current_price": {"usd": 50000},
    ...
  }
}
```

**Error Response:**
- `404`: Coin not found.

---

## Swagger Documentation

Swagger is integrated into the application for interactive API documentation. Once the server is running, access the Swagger UI at:  
`http://127.0.0.1:5000/apidocs`

## Project Structure

```
FlaskServer/
├── flask_server 1.py   # Main Flask application
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Error Handling

The application handles errors gracefully:
- **HTTP Errors:** Returns a JSON response with the error message and status code.
- **Request Errors:** Returns a 500 status code with a descriptive error message.

## Future Enhancements

- Add authentication for secure API access.
- Implement caching for frequently accessed data.
- Add more endpoints for advanced CoinGecko API features.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [CoinGecko API](https://www.coingecko.com/en/api) for cryptocurrency data.
- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [Flasgger](https://github.com/flasgger/flasgger) for Swagger integration.