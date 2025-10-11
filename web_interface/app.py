#!/usr/bin/env python3
"""
NeuTTS-Air Web Interface
Simple Flask web app for text-to-speech synthesis
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, Response, stream_with_context
import soundfile as sf
import json
import time
from queue import Queue
from threading import Thread

# Add parent directory to path to import neuttsair
sys.path.insert(0, str(Path(__file__).parent.parent))
from neuttsair.neutts import NeuTTSAir

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = Path(__file__).parent / 'uploads'
app.config['OUTPUT_FOLDER'] = Path(__file__).parent / 'outputs'
app.config['SAMPLES_FOLDER'] = Path(__file__).parent.parent / 'samples'

# Ensure directories exist
app.config['UPLOAD_FOLDER'].mkdir(exist_ok=True)
app.config['OUTPUT_FOLDER'].mkdir(exist_ok=True)

# Global TTS instance (lazy loaded)
tts_instance = None

# Progress tracking
progress_queues = {}


def get_tts(backbone="neuphonic/neutts-air"):
    """Get or create TTS instance"""
    global tts_instance
    if tts_instance is None:
        print(f"Initializing NeuTTS-Air with backbone: {backbone}")
        tts_instance = NeuTTSAir(
            backbone_repo=backbone,
            backbone_device="cpu",
            codec_repo="neuphonic/neucodec",
            codec_device="cpu"
        )
    return tts_instance


def get_sample_files():
    """Get list of available sample files"""
    samples = []
    sample_dir = app.config['SAMPLES_FOLDER']

    # Find all wav files
    for wav_file in sample_dir.glob('*.wav'):
        name = wav_file.stem
        txt_file = sample_dir / f"{name}.txt"

        # Read text content if available
        txt_content = None
        if txt_file.exists():
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    txt_content = f.read().strip()
            except Exception as e:
                print(f"Error reading {txt_file}: {e}")

        samples.append({
            'name': name,
            'wav': str(wav_file),
            'txt': txt_content
        })

    return samples


@app.route('/')
def index():
    """Main page"""
    samples = get_sample_files()
    return render_template('index.html', samples=samples)


def send_progress(session_id, step, message, progress):
    """Send progress update to client"""
    if session_id in progress_queues:
        progress_queues[session_id].put({
            'step': step,
            'message': message,
            'progress': progress
        })


def synthesize_task(session_id, input_text, ref_text, ref_audio_path, backbone):
    """Background task for synthesis"""
    try:
        # Step 1: Initialize TTS
        send_progress(session_id, 1, 'Initializing TTS engine...', 10)
        tts = get_tts(backbone)

        # Step 2: Encode reference
        send_progress(session_id, 2, 'Encoding reference audio...', 30)
        ref_codes = tts.encode_reference(ref_audio_path)

        # Step 3: Generate speech
        send_progress(session_id, 3, 'Generating speech...', 60)
        wav = tts.infer(input_text, ref_codes, ref_text)

        # Step 4: Save output
        send_progress(session_id, 4, 'Saving audio file...', 90)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"output_{timestamp}.wav"
        output_path = app.config['OUTPUT_FOLDER'] / output_filename
        sf.write(str(output_path), wav, 24000)

        # Complete
        send_progress(session_id, 5, 'Complete!', 100)
        progress_queues[session_id].put({
            'complete': True,
            'output_file': output_filename,
            'message': 'Speech synthesized successfully!'
        })

    except Exception as e:
        progress_queues[session_id].put({
            'error': True,
            'message': str(e)
        })


@app.route('/api/synthesize', methods=['POST'])
def synthesize():
    """Start synthesis and return session ID for progress tracking"""
    try:
        # Get form data
        input_text = request.form.get('input_text', '').strip()
        ref_text = request.form.get('ref_text', '').strip()
        use_sample = request.form.get('use_sample', 'false') == 'true'
        sample_name = request.form.get('sample_name', '')
        backbone = request.form.get('backbone', 'neuphonic/neutts-air')

        if not input_text:
            return jsonify({'error': 'Input text is required'}), 400

        # Get reference audio
        if use_sample and sample_name:
            # Use sample file
            ref_audio_path = str(app.config['SAMPLES_FOLDER'] / f"{sample_name}.wav")
            ref_text_path = str(app.config['SAMPLES_FOLDER'] / f"{sample_name}.txt")

            # Load reference text if not provided
            if not ref_text and Path(ref_text_path).exists():
                with open(ref_text_path, 'r') as f:
                    ref_text = f.read().strip()
        else:
            # Use uploaded file
            if 'ref_audio' not in request.files:
                return jsonify({'error': 'Reference audio is required'}), 400

            ref_audio = request.files['ref_audio']
            if ref_audio.filename == '':
                return jsonify({'error': 'No reference audio selected'}), 400

            # Save uploaded file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"ref_{timestamp}.wav"
            ref_audio_path = str(app.config['UPLOAD_FOLDER'] / filename)
            ref_audio.save(ref_audio_path)

        if not ref_text:
            return jsonify({'error': 'Reference text is required'}), 400

        # Create session ID and progress queue
        session_id = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        progress_queues[session_id] = Queue()

        # Start background task
        thread = Thread(
            target=synthesize_task,
            args=(session_id, input_text, ref_text, ref_audio_path, backbone)
        )
        thread.daemon = True
        thread.start()

        return jsonify({
            'session_id': session_id
        })

    except Exception as e:
        print(f"Error starting synthesis: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/progress/<session_id>')
def progress(session_id):
    """Stream progress updates via Server-Sent Events"""
    def generate():
        if session_id not in progress_queues:
            yield f"data: {json.dumps({'error': 'Invalid session ID'})}\n\n"
            return

        queue = progress_queues[session_id]

        while True:
            try:
                # Get progress update (timeout after 30 seconds)
                update = queue.get(timeout=30)
                yield f"data: {json.dumps(update)}\n\n"

                # If complete or error, clean up and exit
                if update.get('complete') or update.get('error'):
                    del progress_queues[session_id]
                    break

            except:
                # Timeout or error - send keepalive
                yield f"data: {json.dumps({'keepalive': True})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )


@app.route('/api/download/<filename>')
def download(filename):
    """Download generated audio file"""
    try:
        file_path = app.config['OUTPUT_FOLDER'] / filename
        if not file_path.exists():
            return jsonify({'error': 'File not found'}), 404

        return send_file(
            file_path,
            mimetype='audio/wav',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/play/<filename>')
def play(filename):
    """Stream audio file for playback"""
    try:
        file_path = app.config['OUTPUT_FOLDER'] / filename
        if not file_path.exists():
            return jsonify({'error': 'File not found'}), 404

        return send_file(
            file_path,
            mimetype='audio/wav'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/samples')
def list_samples():
    """List available sample files"""
    samples = get_sample_files()
    return jsonify({'samples': samples})


if __name__ == '__main__':
    import os

    # Check if running in production
    is_production = os.environ.get('FLASK_ENV') == 'production'

    print("=" * 60)
    print("NeuTTS-Air Web Interface")
    print("=" * 60)
    print(f"Environment: {'Production' if is_production else 'Development'}")
    print("Starting server on http://0.0.0.0:5000")
    print("Press Ctrl+C to stop")
    print("=" * 60)

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=not is_production,
        threaded=True
    )
