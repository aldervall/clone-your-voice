# NeuTTS Air ☁️ + Web Interface

> **This fork adds a beautiful web interface and Docker support for easy deployment!**

HuggingFace 🤗: [Model](https://huggingface.co/neuphonic/neutts-air), [Q8 GGUF](https://huggingface.co/neuphonic/neutts-air-q8-gguf), [Q4 GGUF](https://huggingface.co/neuphonic/neutts-air-q4-gguf) [Spaces](https://huggingface.co/spaces/neuphonic/neutts-air)

[Original Demo Video](https://github.com/user-attachments/assets/020547bc-9e3e-440f-b016-ae61ca645184)

*Original model created by [Neuphonic](http://neuphonic.com/) - building faster, smaller, on-device voice AI*

State-of-the-art Voice AI has been locked behind web APIs for too long. NeuTTS Air is the world's first super-realistic, on-device, TTS speech language model with instant voice cloning. Built off a 0.5B LLM backbone, NeuTTS Air brings natural-sounding speech, real-time performance, built-in security and speaker cloning to your local device - unlocking a new category of embedded voice agents, assistants, toys, and compliance-safe apps.

## ✨ What's New in This Fork

- 🌐 **Beautiful Web Interface** - Modern, responsive UI with gradient design
- 🐳 **Docker Support** - One-command deployment with docker-compose
- 🎨 **Easy to Use** - No command-line required, just open your browser
- 📦 **Ready to Deploy** - Production-ready configuration included
- 📖 **Comprehensive Docs** - Detailed guides for Docker, web interface, and architecture

**Get started in seconds:**
```bash
git clone https://github.com/aldervall/neutts-air-web.git
cd neutts-air-web
./docker-run.sh
# Open http://localhost:5000
```

## Key Features

- 🗣Best-in-class realism for its size - produces natural, ultra-realistic voices that sound human
- 📱Optimised for on-device deployment - provided in GGML format, ready to run on phones, laptops, or even Raspberry Pis
- 👫Instant voice cloning - create your own speaker with as little as 3 seconds of audio
- 🚄Simple LM + codec architecture built off a 0.5B backbone - the sweet spot between speed, size, and quality for real-world applications

> [!CAUTION]
> Websites like neutts.com are popping up and they're not affliated with Neuphonic, our github or this repo.
>
> We are on neuphonic.com only. Please be careful out there! 🙏

## Model Details

NeuTTS Air is built off Qwen 0.5B - a lightweight yet capable language model optimised for text understanding and generation - as well as a powerful combination of technologies designed for efficiency and quality:
- **Supported Languages**: English
- **Audio Codec**: [NeuCodec](https://huggingface.co/neuphonic/neucodec) - our 50hz neural audio codec that achieves exceptional audio quality at low bitrates using a single codebook
- **Context Window**: 2048 tokens, enough for processing ~30 seconds of audio (including prompt duration)
- **Format**: Available in GGML format for efficient on-device inference
- **Responsibility**: Watermarked outputs
- **Inference Speed**: Real-time generation on mid-range devices
- **Power Consumption**: Optimised for mobile and embedded devices

## 🚀 Quick Start

### Option 1: Docker (Recommended) 🐳

The easiest way to get started - no manual dependency installation required!

```bash
# Clone the repository
git clone https://github.com/aldervall/neutts-air-web.git
cd neutts-air-web

# Build and start with one command
./docker-run.sh

# Or use docker-compose directly
docker-compose up -d
```

**Access the web interface:** Open http://localhost:5000 in your browser

**Features:**
- 🎤 Voice cloning with instant results
- 📝 Text-to-speech synthesis
- 🎵 Live audio playback
- 💾 Download generated audio
- 🧠 Multiple model options

**Manage the container:**
```bash
./docker-run.sh logs      # View logs
./docker-run.sh stop      # Stop container
./docker-run.sh restart   # Restart container
./docker-run.sh status    # Check status
./docker-run.sh clean     # Remove container and image
```

📖 See [DOCKER_README.md](DOCKER_README.md) for detailed Docker documentation.

### Option 2: Web Interface (Python) 🌐

Run the web interface directly with Python:

```bash
# Clone the repository
git clone https://github.com/aldervall/neutts-air-web.git
cd neutts-air-web

# Install espeak (required)
# Mac OS
brew install espeak

# Ubuntu/Debian
sudo apt install espeak

# Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install flask

# Start the web server
cd web_interface
./start.sh
```

**Access the web interface:** Open http://localhost:5000 in your browser

📖 See [web_interface/README.md](web_interface/README.md) for web interface documentation.

### Option 3: Command Line (CLI) 💻

Use the original CLI for scripting and automation:

```bash
# Clone the repository
git clone https://github.com/aldervall/neutts-air-web.git
cd neutts-air-web

# Install espeak
# Mac OS: brew install espeak
# Ubuntu/Debian: sudo apt install espeak
# Windows: See note below

# Install Python dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run basic example
python -m examples.basic_example \
  --input_text "My name is Dave, and um, I'm from London" \
  --ref_audio samples/dave.wav \
  --ref_text samples/dave.txt
```

**Platform-specific espeak setup:**

<details>
<summary>Mac users (click to expand)</summary>

You may need to configure espeak library path:
```python
from phonemizer.backend.espeak.wrapper import EspeakWrapper
_ESPEAK_LIBRARY = '/opt/homebrew/Cellar/espeak/1.48.04_1/lib/libespeak.1.1.48.dylib'
EspeakWrapper.set_library(_ESPEAK_LIBRARY)
```
</details>

<details>
<summary>Windows users (click to expand)</summary>

Configure espeak environment variables:
```pwsh
$env:PHONEMIZER_ESPEAK_LIBRARY = "c:\Program Files\eSpeak NG\libespeak-ng.dll"
$env:PHONEMIZER_ESPEAK_PATH = "c:\Program Files\eSpeak NG"
setx PHONEMIZER_ESPEAK_LIBRARY "c:\Program Files\eSpeak NG\libespeak-ng.dll"
setx PHONEMIZER_ESPEAK_PATH "c:\Program Files\eSpeak NG"
```
</details>

**Optional performance optimizations:**
```bash
# For GGUF models (faster)
pip install llama-cpp-python

# For ONNX decoder
pip install onnxruntime
```

To specify a model, add the `--backbone` argument. Available models: [NeuTTS-Air HuggingFace collection](https://huggingface.co/collections/neuphonic/neutts-air-68cc14b7033b4c56197ef350).

📖 See [QUICK_START.md](QUICK_START.md) for comparison of all methods.

### One-Code Block Usage

```python
from neuttsair.neutts import NeuTTSAir
import soundfile as sf

tts = NeuTTSAir(
   backbone_repo="neuphonic/neutts-air", # or 'neutts-air-q4-gguf' with llama-cpp-python installed
   backbone_device="cpu",
   codec_repo="neuphonic/neucodec",
   codec_device="cpu"
)
input_text = "My name is Dave, and um, I'm from London."

ref_text = "samples/dave.txt"
ref_audio_path = "samples/dave.wav"

ref_text = open(ref_text, "r").read().strip()
ref_codes = tts.encode_reference(ref_audio_path)

wav = tts.infer(input_text, ref_codes, ref_text)
sf.write("test.wav", wav, 24000)
```

## Preparing References for Cloning

NeuTTS Air requires two inputs:

1. A reference audio sample (`.wav` file)
2. A text string

The model then synthesises the text as speech in the style of the reference audio. This is what enables NeuTTS Air’s instant voice cloning capability.

### Example Reference Files

You can find some ready-to-use samples in the `examples` folder:

- `samples/dave.wav`
- `samples/jo.wav`

### Guidelines for Best Results

For optimal performance, reference audio samples should be:

1. **Mono channel**
2. **16-44 kHz sample rate**
3. **3–15 seconds in length**
4. **Saved as a `.wav` file**
5. **Clean** — minimal to no background noise
6. **Natural, continuous speech** — like a monologue or conversation, with few pauses, so the model can capture tone effectively

## Guidelines for minimizing Latency

For optimal performance on-device:

1. Use the GGUF model backbones
2. Pre-encode references
3. Use the [onnx codec decoder](https://huggingface.co/neuphonic/neucodec-onnx-decoder)

Take a look at this example [examples README](examples/README.md###minimal-latency-example) to get started.

## Responsibility

Every audio file generated by NeuTTS Air includes [Perth (Perceptual Threshold) Watermarker](https://github.com/resemble-ai/perth).

## Disclaimer

Don't use this model to do bad things… please.

## Developer Requirements

To run the pre commit hooks to contribute to this project run:

```bash
pip install pre-commit
```
Then:
```bash
pre-commit install
```
