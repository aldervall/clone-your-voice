"""
Main Routes
Homepage and utility routes
"""
from flask import Blueprint, render_template, jsonify
from src.utils.helpers import get_sample_files
from src.config.settings import get_config
from src.config.logging_config import get_logger

logger = get_logger(__name__)

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Main page - streamlined interface"""
    logger.debug("Serving main page")
    config = get_config()
    return render_template('index.html', base_url=config.BASE_URL)


@main_bp.route('/api/samples')
def list_samples():
    """List available sample files"""
    try:
        config = get_config()
        samples = get_sample_files(config.SAMPLES_FOLDER)
        logger.debug(f"Returning {len(samples)} samples")
        return jsonify({'samples': samples})
    except Exception as e:
        logger.error(f"Error listing samples: {e}")
        return jsonify({'error': str(e)}), 500


@main_bp.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'clone-your-voice'
    }), 200
