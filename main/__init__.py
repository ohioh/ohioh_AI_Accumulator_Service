from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
from config import Config

load_dotenv()

mongo = MongoClient(Config.MONGO_URI)

## Clusters
mongo1 = MongoClient(Config.MONGO_1)
mongo2 = MongoClient(Config.MONGO_2)
mongo3 = MongoClient(Config.MONGO_3)
mongo4 = MongoClient(Config.MONGO_4)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    from .routes import api_bp
    app.register_blueprint(api_bp)
    return app


app = create_app(Config)

