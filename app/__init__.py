from flask import Flask
from app.config import SECRET_KEY, DEBUG
from app.models import init_db
from app.blueprints.main import main

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["DEBUG"] = DEBUG
    init_db()
    app.register_blueprint(main)
    return app
