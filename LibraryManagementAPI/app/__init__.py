from flask import Flask
from flasgger import Swagger

def create_app():
    """Application Factory Pattern for creating a Flask app."""
    app = Flask(__name__)

    # Swagger configuration
    app.config['SWAGGER'] = {
        'title': 'Library Management API',
        'uiversion': 3
    }
    Swagger(app)

    # Import and register blueprints
    from app.routes import app as routes_blueprint
    app.register_blueprint(routes_blueprint, url_prefix="/")

    return app
