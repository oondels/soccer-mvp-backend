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
