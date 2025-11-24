"""
Media Routes
Audio file download and playback endpoints
"""
from flask import Blueprint, jsonify, send_file

from src.services.file_manager import get_file_manager
from src.config.settings import get_config
from src.config.logging_config import get_logger

logger = get_logger(__name__)

media_bp = Blueprint('media', __name__, url_prefix='/api')


@media_bp.route('/download/<filename>')
def download(filename):
    """Download generated audio file"""
    try:
        config = get_config()
        file_manager = get_file_manager(
            config.UPLOAD_FOLDER,
            config.OUTPUT_FOLDER,
            config.SAMPLES_FOLDER
        )

        file_path = file_manager.get_output_path(filename)
        if file_path is None:
            logger.warning(f"Download requested for non-existent file: {filename}")
            return jsonify({'error': 'File not found'}), 404

        logger.info(f"Downloading file: {filename}")
        return send_file(
            file_path,
            mimetype='audio/wav',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        return jsonify({'error': str(e)}), 500


@media_bp.route('/play/<filename>')
def play(filename):
    """Stream audio file for playback"""
    try:
        config = get_config()
        file_manager = get_file_manager(
            config.UPLOAD_FOLDER,
            config.OUTPUT_FOLDER,
            config.SAMPLES_FOLDER
        )

        file_path = file_manager.get_output_path(filename)
        if file_path is None:
            logger.warning(f"Playback requested for non-existent file: {filename}")
            return jsonify({'error': 'File not found'}), 404

        logger.debug(f"Streaming file: {filename}")
        return send_file(
            file_path,
            mimetype='audio/wav'
        )

    except Exception as e:
        logger.error(f"Error playing file: {e}")
        return jsonify({'error': str(e)}), 500
