import os
from flasgger import Swagger
from flask import Flask
from flask_migrate import Migrate
from src.api import register_routes
from src.database.db import db
from src.extensions import bcrypt
from src.extensions import login_manager
from dotenv import load_dotenv
from config import config


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "soccer_mvp.db")
SECRET_KEY = os.getenv("SECRET_KEY")

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    app.config.from_object(config[config_name])
    
    login_manager.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    Migrate(app, db)
    Swagger(app)
    
    register_routes(app)

    return app
    