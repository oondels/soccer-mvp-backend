import os
from flasgger import Swagger
from flask import Flask
from flask_migrate import Migrate
from src.routes import register_routes
from src.database.db import db
from src.dependencies import bcrypt
from src.dependencies import login_manager
from dotenv import load_dotenv

from src.database.models.user import User


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "soccer_mvp.db")
SECRET_KEY = os.getenv("SECRET_KEY")

def create_app():
    load_dotenv()
    migrate = Migrate() 
    app = Flask(__name__)
    
    app.secret_key = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET_KEY
    
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    Swagger(app)
    
    register_routes(app)

    return app
    