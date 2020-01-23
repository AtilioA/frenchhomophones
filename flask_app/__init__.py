from flask import Flask
from flask_compress import Compress

from .extensions import mongo
from .views import views


def create_app(config_object='flask_app.settings'):
    """Creates a flask application instance and loads its config from config_object"""

    app = Flask(__name__, static_folder='static')

    app.config.from_object(config_object)

    mongo.init_app(app)

    app.register_blueprint(views)
    Compress(app)

    return app
