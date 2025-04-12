import os
from dotenv import load_dotenv

load_dotenv()

COINGECKO_API = "https://api.coingecko.com/api/v3"
HEADERS = {"accept": "application/json"}
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")