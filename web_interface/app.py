#!/usr/bin/env python3
"""
NeuTTS-Air Web Interface
Simple Flask web app for text-to-speech synthesis
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
import soundfile as sf

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


@app.route('/api/synthesize', methods=['POST'])
def synthesize():
    """Synthesize speech from text"""
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

        # Initialize TTS
        tts = get_tts(backbone)

        # Encode reference
        print(f"Encoding reference audio: {ref_audio_path}")
        ref_codes = tts.encode_reference(ref_audio_path)

        # Generate speech
        print(f"Generating speech for: {input_text[:50]}...")
        wav = tts.infer(input_text, ref_codes, ref_text)

        # Save output
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"output_{timestamp}.wav"
        output_path = app.config['OUTPUT_FOLDER'] / output_filename
        sf.write(str(output_path), wav, 24000)

        print(f"Audio saved to: {output_path}")

        return jsonify({
            'success': True,
            'output_file': output_filename,
            'message': 'Speech synthesized successfully!'
        })

    except Exception as e:
        print(f"Error during synthesis: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


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
