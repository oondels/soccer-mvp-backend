import os
from flasgger import Swagger
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
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
        print(f"Using configuration: {config_name}")
    
    app = Flask(__name__)
    
    app.config.from_object(config[config_name])
    
    # Configurar CORS
    CORS(app, 
         origins=[
             "http://localhost:3000",
             "http://localhost:8000",
             "http://127.0.0.1:3000",
             "http://127.0.0.1:8000",
         ],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization'],
         supports_credentials=True)
    
    login_manager.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    Migrate(app, db)
    
    # Configurar Swagger com OpenAPI 3.0.2
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    
    swagger_template = app.config.get('SWAGGER', {})
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Importar modelos para garantir que as tabelas sejam criadas
    with app.app_context():
        from src.models.teams import Team
        from src.models.team_players import TeamPlayer
        # from src.models.user import User  # Se existir
        db.create_all()
    
    register_routes(app)

    return app
    