import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key')
    MASTER_API_KEY: str = os.getenv('MASTER_API_KEY', '')

    # Database
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: int = int(os.getenv('DB_PORT', 5432))
    DB_NAME: str = os.getenv('DB_NAME', 'auth_service')
    DB_USER: str = os.getenv('DB_USER', 'auth-admin')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', 'auth-admin')

    # SendGrid
    SENDGRID_API_KEY: str = os.getenv('SENDGRID_API_KEY', '')
    EMAIL_FROM: str = os.getenv('EMAIL_FROM', 'noreply@example.com')
    EMAIL_FROM_NAME: str = os.getenv('EMAIL_FROM_NAME', 'Auth Service')

    # Token Expiration (seconds)
    AUTH_TOKEN_EXPIRATION: int = int(os.getenv('AUTH_TOKEN_EXPIRATION', 3600))
    EMAIL_VERIFICATION_EXPIRATION: int = int(os.getenv('EMAIL_VERIFICATION_EXPIRATION', 86400))
    PASSWORD_RESET_EXPIRATION: int = int(os.getenv('PASSWORD_RESET_EXPIRATION', 3600))
    EMAIL_CHANGE_EXPIRATION: int = int(os.getenv('EMAIL_CHANGE_EXPIRATION', 3600))

    # Application
    APP_HOST: str = os.getenv('APP_HOST', '0.0.0.0')
    APP_PORT: int = int(os.getenv('APP_PORT', 5678))


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG: bool = True
    FLASK_ENV: str = 'development'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG: bool = False
    FLASK_ENV: str = 'production'


def get_config() -> Config:
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')

    if env == 'production':
        return ProductionConfig()

    return DevelopmentConfig()
