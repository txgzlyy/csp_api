from flask import Flask
from flask_cors import CORS
from config import config


def create_app(config_name):
    # app = Flask(__name__, static_folder='E:/file_path', static_url_path='/files')
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from app.api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
