from flask import Flask 

from .extensions import mongo
from .main import main

def create_app(config_object='flask_app.settings'):
    """Creates a flask application instance and loads its config from config_object"""
    
    app = Flask(__name__)

    app.config.from_object(config_object)

    mongo.init_app(app)

    app.register_blueprint(main)

    return app
