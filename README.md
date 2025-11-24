# 🎙️ Clone Your Voice 2.0 - Refactored Edition

> **Production-ready voice cloning with clean, maintainable architecture**

The refactored Clone Your Voice brings professional software engineering practices to AI voice cloning: modular code, separation of concerns, comprehensive testing infrastructure, and production-ready deployment.

[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Clean Architecture](https://img.shields.io/badge/Architecture-Clean-success)](https://github.com/aldervall/clone-your-voice)

## 🆕 What's New in the Refactored Edition

### Architecture Improvements
- ✅ **Modular Code Structure** - Separation of concerns with clear boundaries
- ✅ **Service Layer Pattern** - Business logic separated from API routes
- ✅ **Configuration Management** - Environment-based settings
- ✅ **Centralized Logging** - Structured logging throughout
- ✅ **Error Handling** - Consistent error responses
- ✅ **Type Safety** - Data models for requests/responses

### Developer Experience
- ✅ **Testing Infrastructure** - Ready for unit & integration tests
- ✅ **Development Dependencies** - Black, pytest, mypy included
- ✅ **Package Setup** - Installable with setup.py
- ✅ **Documentation** - Well-documented code and APIs
- ✅ **Clean Project Root** - Organized directory structure

## ✨ Features

- 🎤 **Browser Recording** - No microphone setup required
- 🤖 **AI Voice Cloning** - Powered by NeuTTS-Air
- 📝 **Auto-Generated Prompts** - Just read and record
- 🎵 **Text-to-Speech** - Generate speech from any text
- 📱 **Mobile Friendly** - Works on all devices
- 🐳 **Docker Ready** - One-command deployment
- 💾 **Persistent Storage** - Recordings and outputs saved
- 🏗️ **Production Ready** - Clean architecture, logging, error handling

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/aldervall/clone-your-voice.git
cd clone-your-voice

# Start with Docker Compose
docker-compose up -d

# Open in browser
open http://localhost:5000
```

### Option 2: Local Development

```bash
# Clone and setup
git clone https://github.com/aldervall/clone-your-voice.git
cd clone-your-voice

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 📁 Project Structure

```
clone-your-voice/
├── src/                        # All application code
│   ├── api/                    # Flask API layer
│   │   ├── routes/             # Route blueprints
│   │   ├── middleware/         # Error handlers, logging
│   │   └── app.py              # App factory
│   ├── services/               # Business logic
│   │   ├── tts_service.py      # TTS orchestration
│   │   ├── session_manager.py  # Progress tracking
│   │   └── file_manager.py     # File operations
│   ├── tts/                    # TTS engine
│   │   ├── engine.py           # Main TTS class
│   │   ├── encoder.py          # Audio encoding
│   │   ├── decoder.py          # Audio decoding
│   │   ├── phonemizer.py       # Text to phonemes
│   │   └── inference.py        # Model inference
│   ├── models/                 # Data models
│   ├── config/                 # Configuration
│   └── utils/                  # Utilities
├── templates/                  # HTML templates
├── tests/                      # Test suite
├── data/                       # Data storage
│   ├── samples/                # Demo voices
│   ├── uploads/                # User recordings
│   └── outputs/                # Generated audio
├── docker/                     # Docker configs
├── docs/                       # Documentation
├── scripts/                    # Utility scripts
├── main.py                     # Entry point
├── docker-compose.yml          # Docker Compose config
└── requirements.txt            # Dependencies
```

## 🛠️ Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install package in editable mode
pip install -e .
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/test_tts_service.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Check types
mypy src/

# Lint
flake8 src/ tests/
```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
# Flask Environment
FLASK_ENV=development

# Server Configuration
HOST=0.0.0.0
PORT=5000

# TTS Configuration
TTS_BACKBONE_REPO=neuphonic/neutts-air
TTS_BACKBONE_DEVICE=cpu
TTS_MAX_TOKENS=1200

# Logging
LOG_LEVEL=INFO
```

### Configuration Files

- `src/config/settings.py` - Main configuration
- `.env` - Environment-specific overrides
- `docker/docker-compose.yml` - Docker configuration

## 📖 API Documentation

### Endpoints

- `GET /` - Main interface
- `GET /health` - Health check
- `POST /api/synthesize` - Start synthesis
- `GET /api/progress/<session_id>` - Track progress (SSE)
- `GET /api/download/<filename>` - Download audio
- `GET /api/play/<filename>` - Stream audio
- `GET /api/samples` - List sample voices

See `docs/API.md` for detailed API documentation.

## 🐳 Docker Deployment

### Build and Run

```bash
# Build image
docker-compose build

# Run container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop container
docker-compose down
```

### Custom Configuration

Edit `docker-compose.yml` to customize:
- Port mappings
- Volume mounts
- Environment variables
- Resource limits

## 📊 System Requirements

**Minimum:**
- 2 CPU cores
- 2GB RAM
- 5GB disk space

**Recommended:**
- 4 CPU cores
- 4GB RAM
- 10GB disk space

**Note:** No GPU required! Runs on CPU.

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure code quality (black, mypy, flake8)
6. Submit a pull request

## 📝 License

MIT License - see [LICENSE](LICENSE)

## 🙏 Acknowledgments

- [NeuTTS-Air](https://github.com/neuphonic/neutts-air) - Core TTS engine
- [Neuphonic](https://neuphonic.com/) - AI model development

## 📧 Contact

- GitHub: [@aldervall](https://github.com/aldervall)
- Issues: [Report here](https://github.com/aldervall/clone-your-voice/issues)

---

**Clone Your Voice - Refactored Edition** - *Professional AI voice cloning with clean architecture* 🎙️
