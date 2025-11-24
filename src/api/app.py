"""
Flask Application Factory
Creates and configures the Flask application
"""
import os
from flask import Flask
from pathlib import Path

from src.config.settings import get_config
from src.config.logging_config import setup_logging, get_logger
from src.api.middleware.error_handlers import register_error_handlers
from src.api.routes.main import main_bp
from src.api.routes.synthesis import synthesis_bp
from src.api.routes.media import media_bp


def create_app(env: str = None) -> Flask:
    """
    Application factory function

    Args:
        env: Environment name (development, production, testing)
             If None, uses FLASK_ENV environment variable

    Returns:
        Configured Flask application
    """
    # Get configuration
    config = get_config(env)

    # Setup logging
    log_level = os.getenv('LOG_LEVEL', 'INFO' if config.ENV == 'production' else 'DEBUG')
    log_file = os.getenv('LOG_FILE')
    log_file_path = Path(log_file) if log_file else None

    setup_logging(
        level=log_level,
        log_file=log_file_path,
        json_format=(config.ENV == 'production')
    )

    logger = get_logger(__name__)
    logger.info(f"Creating Flask app for environment: {config.ENV}")

    # Create Flask app
    app = Flask(
        __name__,
        template_folder=str(config.BASE_DIR / 'templates'),
        static_folder=str(config.SRC_DIR / 'api' / 'static')
    )

    # Load configuration
    app.config.from_object(config)

    # Additional Flask config
    app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

    # Ensure required directories exist
    config.ensure_directories()

    # Register error handlers
    register_error_handlers(app)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(synthesis_bp)
    app.register_blueprint(media_bp)

    logger.info("Flask application created successfully")
    logger.info(f"Template folder: {app.template_folder}")
    logger.info(f"Static folder: {app.static_folder}")

    return app


def run_app():
    """
    Run the Flask application

    This function is called when running the app directly
    """
    # Get environment
    env = os.getenv('FLASK_ENV', 'development')
    config = get_config(env)

    # Create app
    app = create_app(env)

    # Get logger
    logger = get_logger(__name__)

    # Print startup banner
    print("=" * 60)
    print("NeuTTS-Air Web Interface - Clone Your Voice")
    print("=" * 60)
    print(f"Environment: {config.ENV}")
    print(f"Debug: {config.DEBUG}")
    print(f"Host: {config.HOST}:{config.PORT}")
    print(f"Starting server on http://{config.HOST}:{config.PORT}")
    print("Press Ctrl+C to stop")
    print("=" * 60)

    # Run app
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG,
        threaded=True
    )


if __name__ == '__main__':
    run_app()
