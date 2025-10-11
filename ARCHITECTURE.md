# NeuTTS-Air Web Interface Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        User's Browser                        │
│                     http://localhost:5000                    │
└────────────────────────────┬────────────────────────────────┘
                             │
                             │ HTTP Requests
                             │
┌────────────────────────────▼────────────────────────────────┐
│                   Flask Web Application                      │
│                    (web_interface/app.py)                    │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐        │
│  │   Routes    │  │  Audio      │  │   Sample     │        │
│  │   Handler   │  │  Processing │  │   Manager    │        │
│  └─────────────┘  └─────────────┘  └──────────────┘        │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ TTS API Calls
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                     NeuTTS-Air Engine                        │
│                  (neuttsair/neutts.py)                       │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Backbone   │  │    Codec     │  │  Reference   │      │
│  │    Model     │  │   Encoder    │  │   Encoder    │      │
│  │  (Qwen 0.5B) │  │  (NeuCodec)  │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## File Structure

```
neutts-air/
├── 🐳 Docker Files
│   ├── Dockerfile              # Container definition
│   ├── docker-compose.yml      # Orchestration
│   ├── docker-run.sh          # Management script
│   └── .dockerignore          # Build exclusions
│
├── 🌐 Web Interface
│   └── web_interface/
│       ├── app.py             # Flask application
│       ├── templates/
│       │   └── index.html     # Web UI
│       ├── static/
│       │   └── style.css      # Styling
│       ├── uploads/           # User uploads (persistent)
│       ├── outputs/           # Generated audio (persistent)
│       └── start.sh           # Python startup script
│
├── 🎤 Voice Samples
│   └── samples/
│       ├── dave.wav & dave.txt
│       ├── jo.wav & jo.txt
│       └── niklas.wav & niklas.txt
│
├── 🧠 NeuTTS Engine
│   └── neuttsair/
│       ├── neutts.py          # Main TTS engine
│       └── [model files]      # AI models
│
├── 📚 Examples
│   └── examples/
│       └── basic_example.py   # CLI usage example
│
└── 📖 Documentation
    ├── README.md              # Main project docs
    ├── DOCKER_README.md       # Docker guide
    ├── QUICK_START.md         # Quick start guide
    └── ARCHITECTURE.md        # This file

```

## Data Flow

### 1. Text-to-Speech Generation

```
User Input (Browser)
    │
    ├─ Text: "Hello world"
    ├─ Reference Audio: niklas.wav
    └─ Reference Text: "Det finns en sak..."
    │
    ▼
Flask Server (app.py)
    │
    ├─ Validate inputs
    ├─ Load/save files
    └─ Initialize TTS engine
    │
    ▼
NeuTTS Engine (neutts.py)
    │
    ├─ Encode reference audio → codes
    ├─ Process input text
    └─ Generate speech using backbone model
    │
    ▼
Audio Output
    │
    ├─ Save as WAV file (24kHz)
    ├─ Apply Perth watermark
    └─ Return to web interface
    │
    ▼
User Browser
    │
    ├─ Play audio
    └─ Download option
```

## Docker Architecture

### Container Layout

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Container                          │
│                  (neutts-air-web)                            │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Python 3.11 Environment                            │    │
│  │                                                       │    │
│  │  ┌──────────────────────────────────────────┐      │    │
│  │  │  Flask App (Port 5000)                   │      │    │
│  │  │  - Routes handling                       │      │    │
│  │  │  - Audio processing                      │      │    │
│  │  │  - Model management                      │      │    │
│  │  └──────────────────────────────────────────┘      │    │
│  │                                                       │    │
│  │  ┌──────────────────────────────────────────┐      │    │
│  │  │  NeuTTS Engine                           │      │    │
│  │  │  - Backbone model (CPU)                  │      │    │
│  │  │  - Codec model (CPU)                     │      │    │
│  │  └──────────────────────────────────────────┘      │    │
│  │                                                       │    │
│  │  Dependencies:                                        │    │
│  │  - espeak (phonemizer)                               │    │
│  │  - libsndfile (audio I/O)                           │    │
│  │  - torch, transformers, etc.                         │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                               │
│  Volume Mounts:                                              │
│  /app/web_interface/uploads  ← → ./web_interface/uploads    │
│  /app/web_interface/outputs  ← → ./web_interface/outputs    │
│  /app/samples (read-only)    ← → ./samples                  │
│                                                               │
│  Port Mapping:                                               │
│  Container:5000 → Host:5000                                  │
└─────────────────────────────────────────────────────────────┘
```

### Volume Persistence

```
Host Machine                    Docker Container
─────────────                   ─────────────────

./web_interface/uploads   ←→   /app/web_interface/uploads
    (User uploaded audio)       (Read/Write)

./web_interface/outputs   ←→   /app/web_interface/outputs
    (Generated audio)           (Read/Write)

./samples                 ←→   /app/samples
    (Sample voices)             (Read-Only)
```

## API Endpoints

### HTTP Routes

```
GET  /                          → Main web interface
POST /api/synthesize           → Generate speech
GET  /api/play/<filename>      → Stream audio
GET  /api/download/<filename>  → Download audio
GET  /api/samples              → List available samples
```

### Request/Response Flow

```
POST /api/synthesize
├─ Input:
│  ├─ input_text: "Text to synthesize"
│  ├─ ref_text: "Reference transcript"
│  ├─ ref_audio: file or sample name
│  ├─ backbone: model selection
│  └─ use_sample: true/false
│
└─ Output:
   ├─ success: true
   ├─ output_file: "output_20251011_123456.wav"
   └─ message: "Speech synthesized successfully!"
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│ Frontend Layer                                               │
├─────────────────────────────────────────────────────────────┤
│ • HTML5 + CSS3 (Responsive Design)                          │
│ • Vanilla JavaScript (Fetch API)                            │
│ • Audio Player (HTML5 <audio>)                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Backend Layer                                                │
├─────────────────────────────────────────────────────────────┤
│ • Flask 3.1 (Web Framework)                                 │
│ • Python 3.11+ (Runtime)                                    │
│ • soundfile (Audio I/O)                                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ AI/ML Layer                                                  │
├─────────────────────────────────────────────────────────────┤
│ • NeuTTS-Air (TTS Engine)                                   │
│ • Qwen 0.5B (Backbone LLM)                                  │
│ • NeuCodec (Audio Codec)                                    │
│ • PyTorch (ML Framework)                                    │
│ • Transformers (Model Loading)                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Infrastructure Layer                                         │
├─────────────────────────────────────────────────────────────┤
│ • Docker (Containerization)                                 │
│ • Docker Compose (Orchestration)                            │
│ • espeak-ng (Phonemization)                                 │
└─────────────────────────────────────────────────────────────┘
```

## Security Considerations

### Built-in Security Features

- ✅ File type validation (WAV only)
- ✅ File size limits (50MB max)
- ✅ Output watermarking (Perth)
- ✅ Read-only sample mounts
- ✅ Isolated container environment

### Recommended Additional Security

- 🔒 Add authentication/authorization
- 🔒 Rate limiting for API endpoints
- 🔒 HTTPS with reverse proxy
- 🔒 Input sanitization
- 🔒 CORS configuration

## Performance Characteristics

### Resource Usage

```
CPU Usage:    High during generation (100% single core)
Memory:       ~2-4GB (models + runtime)
Disk Space:   ~5GB (models + cache)
Network:      Minimal (local processing)
```

### Timing

```
First Request:  5-10 seconds (model loading)
Subsequent:     2-5 seconds per generation
Model Cache:    Persists across requests
```

## Scalability Options

### Horizontal Scaling

```
                    ┌──────────────┐
                    │ Load Balancer│
                    └───────┬──────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
        ┌───▼───┐       ┌───▼───┐       ┌───▼───┐
        │ TTS-1 │       │ TTS-2 │       │ TTS-3 │
        │ :5001 │       │ :5002 │       │ :5003 │
        └───────┘       └───────┘       └───────┘
```

### Vertical Scaling

- Add GPU support for faster inference
- Increase memory for larger models
- Use GGUF quantized models (Q4/Q8)

## Monitoring Points

```
Application Level:
├─ Request count
├─ Generation time
├─ Error rate
└─ Active models

System Level:
├─ CPU usage
├─ Memory usage
├─ Disk I/O
└─ Container health

Business Level:
├─ User uploads
├─ Generated files
├─ Popular voices
└─ Model usage
```
