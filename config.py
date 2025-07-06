import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class"""
    
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_HOURS = 24

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_NAME = "soccer_mvp.db"
    DB_PATH = os.path.join(BASE_DIR, "database", DATABASE_NAME)

    JWT_COOKIE_SECURE = True
    JWT_COOKIE_HTTPONLY = True
    JWT_COOKIE_SAMESITE = "Strict"
    
    # Swagger Configuration
    SWAGGER = {
        'title': 'Soccer MVP API',
        'uiversion': 3,
        'openapi': '3.0.2',
        'description': 'API para gerenciamento de equipes de futebol',
        'version': '1.0.0',
        'termsOfService': '',
        'contact': {
            'name': 'Soccer MVP Team',
            'email': 'support@soccermvp.com'
        },
        'license': {
            'name': 'MIT',
            'url': 'https://opensource.org/licenses/MIT'
        },
        'servers': [
            {
                'url': 'http://localhost:5000',
                'description': 'Development server'
            }
        ],
        'tags': [
            {
                'name': 'Teams',
                'description': 'Operações relacionadas a equipes'
            },
            {
                'name': 'Users',
                'description': 'Operações relacionadas a usuários'
            },
            {
                'name': 'Auth',
                'description': 'Operações de autenticação'
            }
        ]
    }


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(Config.BASE_DIR, "src", "database", Config.DATABASE_NAME)}'
    JWT_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Production configuration"""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f'sqlite:///{os.path.join(Config.BASE_DIR, "src", "database", Config.DATABASE_NAME)}',
    )

# Mapeamento de ambientes
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
