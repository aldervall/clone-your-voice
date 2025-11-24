"""
Application Configuration Settings
Centralized configuration management for the voice cloning application
"""
import os
from pathlib import Path
from typing import Optional


class BaseConfig:
    """Base configuration with common settings"""

    # Application
    APP_NAME = "Clone Your Voice"
    APP_VERSION = "2.0"

    # Paths - relative to project root
    BASE_DIR = Path(__file__).parent.parent.parent.resolve()
    SRC_DIR = BASE_DIR / "src"
    DATA_DIR = BASE_DIR / "data"

    # Flask settings
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size

    # Directory paths
    UPLOAD_FOLDER = DATA_DIR / "uploads"
    OUTPUT_FOLDER = DATA_DIR / "outputs"
    SAMPLES_FOLDER = DATA_DIR / "samples"

    # TTS Model Configuration
    TTS_BACKBONE_REPO = os.getenv("TTS_BACKBONE_REPO", "neuphonic/neutts-air")
    TTS_BACKBONE_DEVICE = os.getenv("TTS_BACKBONE_DEVICE", "cpu")
    TTS_CODEC_REPO = os.getenv("TTS_CODEC_REPO", "neuphonic/neucodec")
    TTS_CODEC_DEVICE = os.getenv("TTS_CODEC_DEVICE", "cpu")

    # TTS Processing Settings
    TTS_MAX_TOKENS = int(os.getenv("TTS_MAX_TOKENS", "1200"))
    TTS_SAMPLE_RATE = 24000
    TTS_MAX_CONTEXT = 2048

    # Session Management
    SESSION_TIMEOUT_SECONDS = int(os.getenv("SESSION_TIMEOUT_SECONDS", "300"))
    SESSION_CLEANUP_INTERVAL = int(os.getenv("SESSION_CLEANUP_INTERVAL", "60"))

    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "5000"))
    BASE_URL = os.getenv("BASE_URL", "")

    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist"""
        cls.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
        cls.OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
        cls.SAMPLES_FOLDER.mkdir(parents=True, exist_ok=True)


class DevelopmentConfig(BaseConfig):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False
    ENV = "development"


class ProductionConfig(BaseConfig):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False
    ENV = "production"

    # Override with strong secret key in production
    SECRET_KEY = os.getenv("SECRET_KEY")

    @classmethod
    def validate(cls):
        """Validate production configuration"""
        import os
        # Only validate if actually running in production (not during testing/import)
        if os.getenv('FLASK_RUN_FROM_CLI') or os.getenv('WERKZEUG_RUN_MAIN'):
            if not cls.SECRET_KEY or cls.SECRET_KEY == "dev-secret-key-change-in-production":
                raise ValueError("SECRET_KEY must be set in production environment")


class TestingConfig(BaseConfig):
    """Testing environment configuration"""
    DEBUG = True
    TESTING = True
    ENV = "testing"

    # Use temporary directories for testing
    UPLOAD_FOLDER = Path("/tmp/clone-voice-test/uploads")
    OUTPUT_FOLDER = Path("/tmp/clone-voice-test/outputs")


# Configuration factory
_config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config(env: Optional[str] = None):
    """
    Get configuration based on environment

    Args:
        env: Environment name (development, production, testing)
             If None, uses FLASK_ENV environment variable

    Returns:
        Configuration class
    """
    if env is None:
        env = os.getenv("FLASK_ENV", "development")

    config_class = _config_map.get(env, DevelopmentConfig)

    # Ensure directories exist
    config_class.ensure_directories()

    # Validate production config
    if env == "production":
        config_class.validate()

    return config_class
