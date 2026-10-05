from flask import Flask
from .config import Config


def create_app(config_class=Config):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(config_class)

    from .routes.web import web_bp
    from .routes.api import api_bp
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    return app
