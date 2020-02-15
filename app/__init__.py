from flask import Flask
from config import config_options
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES

bootstrap = Bootstrap()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.writer_login'
photos = UploadSet('photos', IMAGES)


def create_app(config_name):
    """Create an Flask object called app"""
    app = Flask(__name__)

    app.config.from_object(config_options[config_name])

    """Initializing the extensions"""
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    """Register the blueprints"""
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .request import configure_request
    configure_request(app)

    configure_uploads(app, photos)

    return app
