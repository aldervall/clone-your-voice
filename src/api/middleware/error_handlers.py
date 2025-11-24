"""
Error Handlers
Centralized error handling for Flask application
"""
from flask import jsonify
from werkzeug.exceptions import HTTPException
from src.config.logging_config import get_logger

logger = get_logger(__name__)


def register_error_handlers(app):
    """
    Register error handlers with Flask app

    Args:
        app: Flask application instance
    """

    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request"""
        logger.warning(f"Bad request: {error}")
        return jsonify({
            "error": "Bad Request",
            "message": str(error)
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found"""
        logger.warning(f"Not found: {error}")
        return jsonify({
            "error": "Not Found",
            "message": "The requested resource was not found"
        }), 404

    @app.errorhandler(413)
    def request_entity_too_large(error):
        """Handle 413 Request Entity Too Large"""
        logger.warning(f"File too large: {error}")
        return jsonify({
            "error": "File Too Large",
            "message": "The uploaded file is too large. Maximum size is 50MB."
        }), 413

    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server Error"""
        logger.error(f"Internal server error: {error}", exc_info=True)
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later."
        }), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle uncaught exceptions"""
        # Pass through HTTP errors
        if isinstance(error, HTTPException):
            return error

        # Log and return 500 for other exceptions
        logger.error(f"Unhandled exception: {error}", exc_info=True)
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later."
        }), 500
