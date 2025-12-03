# ===============================================================================
# CONFIG AutoGuardEC - Car Insurance Management System
# ===============================================================================

import os
from dotenv import load_dotenv

load_dotenv()

# Base configuration class
# ===============================================================================
class Config:
    # Flask configuration
    # ===============================================================================
    JSON_AS_ASCII = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database configuration - Connection with docker
    # ===============================================================================
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:{os.getenv('DB_PASSWORD', '123')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3308')}/{os.getenv('DB_NAME', 'CarInsuranceDB')}?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OpenAI configuration - Maybe a future implementation
    # OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


# Development configuration
# ===============================================================================
class DevelopmentConfig(Config):
    DEBUG = True

# Production configuration
# ===============================================================================
class ProductionConfig(Config):
    DEBUG = False


# Configuration dictionary
# ===============================================================================
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
