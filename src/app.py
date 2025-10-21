import os
from flask import Flask
from flask_cors import CORS
from config import get_config


def create_app() -> Flask:
    """Application factory pattern"""
    app = Flask(__name__)

    # Load configuration
    config = get_config()
    app.config.from_object(config)

    # Enable CORS - Allow all origins for multi-tenant architecture
    # In production, configure allowed origins via CORS_ORIGINS environment variable
    cors_origins = os.getenv('CORS_ORIGINS', '*')
    if cors_origins == '*':
        CORS(app)
    else:
        # Comma-separated list of allowed origins
        CORS(app, origins=cors_origins.split(','))

    # Register blueprints
    from api.register import register_bp
    from api.login import login_bp
    from api.logout import logout_bp
    from api.verify_email import verify_email_bp
    from api.change_password import change_password_bp
    from api.request_password_reset import request_password_reset_bp
    from api.reset_password import reset_password_bp
    from api.request_email_change import request_email_change_bp
    from api.confirm_email_change import confirm_email_change_bp
    from api.create_site import create_site_bp
    from api.get_site import get_site_bp
    from api.list_sites import list_sites_bp
    from api.update_site import update_site_bp

    app.register_blueprint(register_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(verify_email_bp)
    app.register_blueprint(change_password_bp)
    app.register_blueprint(request_password_reset_bp)
    app.register_blueprint(reset_password_bp)
    app.register_blueprint(request_email_change_bp)
    app.register_blueprint(confirm_email_change_bp)
    app.register_blueprint(create_site_bp)
    app.register_blueprint(get_site_bp)
    app.register_blueprint(list_sites_bp)
    app.register_blueprint(update_site_bp)

    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy', 'service': 'auth-service'}, 200

    return app


if __name__ == '__main__':
    app = create_app()
    config = get_config()
    app.run(host=config.APP_HOST, port=config.APP_PORT, debug=config.DEBUG)
