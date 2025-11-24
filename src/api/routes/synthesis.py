"""
Synthesis Routes
TTS synthesis and progress tracking endpoints
"""
import json
from flask import Blueprint, request, jsonify, Response, stream_with_context
from pathlib import Path

from src.models.synthesis_request import SynthesisRequest
from src.services.session_manager import get_session_manager
from src.services.tts_service import get_tts_service
from src.services.file_manager import get_file_manager
from src.utils.validators import validate_text_input, validate_sample_name
from src.utils.helpers import generate_session_id
from src.config.settings import get_config
from src.config.logging_config import get_logger

logger = get_logger(__name__)

synthesis_bp = Blueprint('synthesis', __name__, url_prefix='/api')


@synthesis_bp.route('/synthesize', methods=['POST'])
def synthesize():
    """Start synthesis and return session ID for progress tracking"""
    try:
        config = get_config()
        session_manager = get_session_manager(config.SESSION_TIMEOUT_SECONDS)
        file_manager = get_file_manager(
            config.UPLOAD_FOLDER,
            config.OUTPUT_FOLDER,
            config.SAMPLES_FOLDER
        )

        # Get form data
        input_text = request.form.get('input_text', '').strip()
        ref_text = request.form.get('ref_text', '').strip()
        use_sample = request.form.get('use_sample', 'false') == 'true'
        sample_name = request.form.get('sample_name', '')
        language = request.form.get('language', 'en-us')

        # Validate input text
        is_valid, error_msg = validate_text_input(input_text, field_name="Input text")
        if not is_valid:
            return jsonify({'error': error_msg}), 400

        # Get reference audio
        if use_sample and sample_name:
            # Use sample file
            is_valid, error_msg = validate_sample_name(sample_name, config.SAMPLES_FOLDER)
            if not is_valid:
                return jsonify({'error': error_msg}), 400

            ref_audio_path = file_manager.get_sample_path(sample_name)
            if ref_audio_path is None:
                return jsonify({'error': f'Sample not found: {sample_name}'}), 404

            # Load reference text if not provided
            if not ref_text:
                ref_text = file_manager.get_sample_text(sample_name)
                if not ref_text:
                    return jsonify({'error': 'Reference text is required'}), 400
        else:
            # Use uploaded file
            if 'ref_audio' not in request.files:
                return jsonify({'error': 'Reference audio is required'}), 400

            ref_audio = request.files['ref_audio']
            if ref_audio.filename == '':
                return jsonify({'error': 'No reference audio selected'}), 400

            # Save uploaded file
            success, ref_audio_path, error_msg = file_manager.save_uploaded_audio(ref_audio)
            if not success:
                return jsonify({'error': error_msg}), 400

        # Validate reference text
        is_valid, error_msg = validate_text_input(ref_text, field_name="Reference text")
        if not is_valid:
            return jsonify({'error': error_msg}), 400

        # Create session
        session_id = generate_session_id()
        session_manager.create_session(session_id)

        # Create synthesis request
        synthesis_request = SynthesisRequest(
            input_text=input_text,
            ref_text=ref_text,
            ref_audio_path=ref_audio_path,
            backbone=config.TTS_BACKBONE_REPO,
            max_tokens=config.TTS_MAX_TOKENS,
            session_id=session_id,
            language=language
        )

        # Start synthesis in background
        tts_service = get_tts_service(
            session_manager=session_manager,
            output_folder=config.OUTPUT_FOLDER,
            backbone_repo=config.TTS_BACKBONE_REPO,
            backbone_device=config.TTS_BACKBONE_DEVICE,
            codec_repo=config.TTS_CODEC_REPO,
            codec_device=config.TTS_CODEC_DEVICE
        )
        tts_service.synthesize_async(synthesis_request)

        logger.info(f"Started synthesis for session: {session_id}")
        return jsonify({'session_id': session_id})

    except Exception as e:
        logger.error(f"Error starting synthesis: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@synthesis_bp.route('/progress/<session_id>')
def progress(session_id):
    """Stream progress updates via Server-Sent Events"""
    def generate():
        config = get_config()
        session_manager = get_session_manager(config.SESSION_TIMEOUT_SECONDS)

        if session_manager.get_session(session_id) is None:
            yield f"data: {json.dumps({'error': 'Invalid session ID'})}\n\n"
            return

        while True:
            try:
                # Get progress update (timeout after 30 seconds)
                update = session_manager.get_progress(session_id, timeout=30)
                yield f"data: {json.dumps(update)}\n\n"

                # If complete or error, clean up and exit
                if update.get('complete') or update.get('error'):
                    session_manager.delete_session(session_id)
                    break

            except Exception as e:
                logger.error(f"Error in progress stream: {e}")
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
                break

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )
