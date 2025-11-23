"""
Configuration settings for the Flask application.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class."""
    
    # Flask configuration
    JSON_AS_ASCII = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI',
        'mysql+pymysql://root:123@localhost:3307/CarInsuranceDB?charset=utf8mb4'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OpenAI configuration (for future use)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
