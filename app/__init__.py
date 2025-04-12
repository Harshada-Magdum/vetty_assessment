from flask import Flask
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from .config import SECRET_KEY, JWT_SECRET_KEY

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

    # Swagger Configuration
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "CoinGecko API Wrapper",
            "description": "API with JWT Auth & Swagger",
            "version": "1.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT token. Format: Bearer <token>"
            }
        },
        "security": [{"Bearer": []}]
    }
    Swagger(app, template=swagger_template)

    # JWT Manager
    JWTManager(app)

    # Register Blueprints
    from .routes import routes_bp
    from .auth import auth_bp
    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp)

    return app

