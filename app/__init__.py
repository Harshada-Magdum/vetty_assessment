from flask import Flask
from flasgger import Swagger
from .routes import bp as main_bp
from .config import swagger_template

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)

    Swagger(app, template=swagger_template)

    return app

