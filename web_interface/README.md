# NeuTTS-Air Web Interface

A simple web interface for NeuTTS-Air text-to-speech with voice cloning capabilities.

## Features

- 🎤 **Voice Cloning**: Use pre-loaded sample voices or upload your own
- 📝 **Text-to-Speech**: Convert any text to speech in the selected voice
- 🎵 **Audio Playback**: Listen to generated audio directly in the browser
- 💾 **Download**: Save generated audio files as WAV
- 🧠 **Model Selection**: Choose between different model variants (standard, Q4, Q8)

## Quick Start

1. **Activate the virtual environment:**
   ```bash
   cd /home/amdvall/neutts-air
   source .venv/bin/activate
   ```

2. **Start the web server:**
   ```bash
   cd web_interface
   python app.py
   ```

3. **Open in browser:**
   Open http://localhost:5000 in your web browser

## Using the Interface

### Using Sample Voices

1. Select "Use Sample Voice"
2. Choose a voice from the dropdown (dave, jo, niklas)
3. The reference text will load automatically
4. Enter the text you want to synthesize
5. Click "Generate Speech"

### Using Custom Voice

1. Select "Upload Custom Voice"
2. Upload a WAV file (3-15 seconds recommended)
3. Enter the transcript of the uploaded audio in "Reference Text"
4. Enter the text you want to synthesize
5. Click "Generate Speech"

### Voice File Requirements

For best results, your reference audio should:
- Be mono channel
- Have 16-44 kHz sample rate
- Be 3–15 seconds in length
- Be saved as a `.wav` file
- Have minimal background noise
- Contain natural, continuous speech

## Directory Structure

```
web_interface/
├── app.py              # Flask application
├── templates/
│   └── index.html      # Web interface
├── static/
│   └── style.css       # Styles
├── uploads/            # Uploaded reference audio
└── outputs/            # Generated audio files
```

## Models Available

- **Standard (neutts-air)**: Best quality, slower
- **Q4 GGUF**: Faster, lower quality (requires llama-cpp-python)
- **Q8 GGUF**: Balanced speed and quality (requires llama-cpp-python)

## Troubleshooting

### Port already in use
If port 5000 is already in use, you can change it in `app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Change 5000 to 5001
```

### Model not loading
Make sure you're in the virtual environment and all dependencies are installed:
```bash
source ../.venv/bin/activate
pip install -r ../requirements.txt
pip install flask
```

### Audio not generating
Check the console output for errors. Common issues:
- Reference audio format not supported (use WAV)
- Missing reference text
- GPU/CPU compatibility issues

## Credits

- Built on [NeuTTS-Air](https://huggingface.co/neuphonic/neutts-air) by [Neuphonic](https://neuphonic.com)
- Web interface powered by Flask
