# 🎙️ Clone Your Voice

> **AI-powered voice cloning made simple**

Record your voice for 10 seconds, then generate speech in your cloned voice with any text. Browser-based recording, no microphone setup required.

[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Features

- 🎤 **Browser Recording** - No microphone setup, record directly in your browser
- 🤖 **AI Voice Cloning** - Powered by NeuTTS-Air (Qwen 0.5B backbone)
- 📝 **Auto-Generated Prompts** - Read a random sentence, we handle the rest
- 🎵 **Text-to-Speech** - Generate speech from any text in your voice
- 📱 **Mobile Friendly** - Works on phones, tablets, and desktops
- 🐳 **Docker Ready** - One-command deployment
- 💾 **Persistent Storage** - Your recordings and outputs are saved

## 🚀 Quick Start

### Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/aldervall/clone-your-voice.git
cd clone-your-voice

# Start with Docker Compose
docker-compose up -d

# Open in browser
open http://localhost:5000
```

**That's it!** The interface is ready to use.

See [QUICKSTART.md](QUICKSTART.md) for more details.

## 🎯 How It Works

### 3 Simple Steps

**Step 1: Record Your Voice** (10 seconds)
- Click the microphone button
- Read the displayed prompt aloud
- Preview your recording

**Step 2: Generate Speech**
- Type any text you want to hear
- Click "Generate Speech"
- Wait for AI processing (~10-30 seconds)

**Step 3: Download**
- Listen to your generated audio
- Download the file
- Generate more!

## 📖 Documentation

- [Quick Start Guide](QUICKSTART.md) - Get running in 5 minutes
- [Docker Deployment](DOCKER_DEPLOYMENT.md) - Complete deployment guide

## 🛠️ Technology Stack

- **AI Model**: [NeuTTS-Air](https://github.com/neuphonic/neutts-air) - Qwen 0.5B backbone
- **Audio Codec**: NeuCodec (50Hz neural codec)
- **Backend**: Python 3.11 + Flask
- **Frontend**: Vanilla JavaScript + CSS
- **Deployment**: Docker + Docker Compose

## 📊 System Requirements

**Minimum:**
- 2 CPU cores, 2GB RAM, 5GB disk

**Recommended:**
- 4 CPU cores, 4GB RAM, 10GB disk

**Note:** No GPU required! Runs on CPU.

## 🐛 Troubleshooting

See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for detailed troubleshooting.

Common issues:
- **Port in use**: Change port in `docker-compose.yml`
- **Out of memory**: Increase memory limit in `docker-compose.yml`
- **Slow generation**: First run takes longer (model loading)

## 🤝 Contributing

Contributions welcome! Fork, make changes, submit PR.

## 📝 License

MIT License - see [LICENSE](LICENSE)

## 🙏 Acknowledgments

- [NeuTTS-Air](https://github.com/neuphonic/neutts-air) - Core TTS engine
- [Neuphonic](https://neuphonic.com/) - AI model development

## 📧 Contact

- GitHub: [@aldervall](https://github.com/aldervall)
- Issues: [Report here](https://github.com/aldervall/clone-your-voice/issues)

---

**Clone Your Voice** - *AI-powered voice cloning made simple* 🎙️
