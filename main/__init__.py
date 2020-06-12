from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
from config import Config

load_dotenv()

mongo = MongoClient(Config.MONGO_URI)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    from .routes import api_bp
    app.register_blueprint(api_bp)
    return app

app = create_app(Config)

