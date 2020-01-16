# WSGI server used by Heroku for production deployment
from flask_app import create_app

app = create_app()
