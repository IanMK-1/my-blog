from flask import Flask
from config import config_options
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()


def create_app(config_name):
    """Create an Flask object called app"""
    app = Flask(__name__)

    app.config.from_object(config_options[config_name])

    """Initializing the extensions"""
    bootstrap.init_app(app)

    """Register the blueprints"""
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .request import configure_request
    configure_request(app)

    return app