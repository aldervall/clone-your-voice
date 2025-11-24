# 📘 Migration Guide - Old to New Structure

This guide helps you understand the mapping between the old monolithic structure and the new refactored architecture.

---

## 🗺️ File Location Mapping

### Old Location → New Location

#### Main Application
```
OLD: web_interface/app.py
NEW: Distributed across:
  - src/api/app.py (app factory)
  - src/api/routes/main.py (homepage)
  - src/api/routes/synthesis.py (synthesis endpoints)
  - src/api/routes/media.py (download/play endpoints)
  - src/services/tts_service.py (synthesis logic)
  - src/services/session_manager.py (progress tracking)
  - src/services/file_manager.py (file operations)
```

#### TTS Engine
```
OLD: neuttsair/neutts.py
NEW: Distributed across:
  - src/tts/engine.py (main NeuTTSAir class)
  - src/tts/encoder.py (encode_reference)
  - src/tts/decoder.py (_decode)
  - src/tts/phonemizer.py (_to_phones)
  - src/tts/inference.py (inference logic)
  - src/tts/streaming.py (streaming inference)
  - src/tts/utils.py (_linear_overlap_add)
```

#### Templates
```
OLD: web_interface/templates/index_new.html
NEW: templates/index.html (cleaned, single template)

REMOVED: web_interface/templates/index.html (old duplicate)
```

#### Static Files
```
OLD: web_interface/static/style.css
NEW: src/api/static/style.css
```

#### Sample Data
```
OLD: samples/
NEW: data/samples/
```

#### Scripts
```
OLD: BUILD_AND_RUN.sh, COMPARE_BUILDS.sh (root)
NEW: scripts/BUILD_AND_RUN.sh, scripts/COMPARE_BUILDS.sh
```

#### Documentation
```
OLD: DOCKER_DEPLOYMENT.md, QUICKSTART.md, etc. (root)
NEW: docs/DOCKER_DEPLOYMENT.md, docs/QUICKSTART.md, etc.
```

#### Docker Files
```
OLD: Dockerfile, docker-compose.yml (root)
NEW: docker/Dockerfile, docker/docker-compose.yml
     (with docker-compose.yml symlink in root for convenience)
```

---

## 🔄 Function Mapping

### Old Function → New Location

#### From `web_interface/app.py`:

| Old Function | New Location | Notes |
|--------------|--------------|-------|
| `get_tts()` | `src/services/tts_service.get_tts_engine()` | Now part of service |
| `get_sample_files()` | `src/utils/helpers.get_sample_files()` | Utility function |
| `index()` | `src/api/routes/main.index()` | Route handler |
| `synthesize()` | `src/api/routes/synthesis.synthesize()` | Route handler |
| `progress()` | `src/api/routes/synthesis.progress()` | Route handler |
| `download()` | `src/api/routes/media.download()` | Route handler |
| `play()` | `src/api/routes/media.play()` | Route handler |
| `list_samples()` | `src/api/routes/main.list_samples()` | Route handler |
| `split_text_into_chunks()` | `src/utils/text_processor.split_text_into_chunks()` | Utility |
| `synthesize_task()` | `src/services/tts_service.synthesize()` | Service method |
| `send_progress()` | `src/services/session_manager.send_progress()` | Service method |

#### From `neuttsair/neutts.py`:

| Old Function | New Location | Notes |
|--------------|--------------|-------|
| `NeuTTSAir.__init__()` | `src/tts/engine.NeuTTSAir.__init__()` | Main class |
| `NeuTTSAir.infer()` | `src/tts/engine.NeuTTSAir.infer()` | Main method |
| `NeuTTSAir.infer_stream()` | `src/tts/engine.NeuTTSAir.infer_stream()` | Streaming |
| `NeuTTSAir.encode_reference()` | `src/tts/encoder.ReferenceEncoder.encode()` | Encoder class |
| `NeuTTSAir._decode()` | `src/tts/decoder.SpeechDecoder.decode()` | Decoder class |
| `NeuTTSAir._to_phones()` | `src/tts/phonemizer.Phonemizer.phonemize()` | Phonemizer class |
| `NeuTTSAir._infer_torch()` | `src/tts/inference.TorchInference.infer()` | Inference class |
| `NeuTTSAir._infer_ggml()` | `src/tts/inference.GGMLInference.infer()` | Inference class |
| `_linear_overlap_add()` | `src/tts/utils.linear_overlap_add()` | Utility function |

---

## 🔌 Import Statements

### How to Update Your Imports

#### Old Style (won't work anymore):
```python
from neuttsair.neutts import NeuTTSAir
from web_interface.app import app
```

#### New Style:
```python
# TTS Engine
from src.tts.engine import NeuTTSAir

# Services
from src.services.tts_service import TTSService, get_tts_service
from src.services.session_manager import SessionManager, get_session_manager
from src.services.file_manager import FileManager, get_file_manager

# Configuration
from src.config.settings import get_config
from src.config.logging_config import setup_logging, get_logger

# Models
from src.models.synthesis_request import SynthesisRequest
from src.models.synthesis_response import SynthesisResult

# Utilities
from src.utils.text_processor import split_text_into_chunks
from src.utils.validators import validate_audio_file, validate_text_input
from src.utils.helpers import get_sample_files

# Flask App
from src.api.app import create_app, run_app
```

---

## ⚙️ Configuration Changes

### Old Configuration (hardcoded):
```python
# In web_interface/app.py
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
UPLOAD_FOLDER = Path(__file__).parent / 'uploads'
```

### New Configuration (centralized):
```python
# Use environment-based config
from src.config.settings import get_config

config = get_config()  # Automatically detects environment
max_size = config.MAX_CONTENT_LENGTH
upload_folder = config.UPLOAD_FOLDER
```

### Environment Variables (.env file):
```bash
# Old: No environment variables
# New: Create .env file (copy from .env.example)
FLASK_ENV=development
HOST=0.0.0.0
PORT=5000
TTS_BACKBONE_REPO=neuphonic/neutts-air
TTS_MAX_TOKENS=1200
LOG_LEVEL=INFO
```

---

## 🐳 Docker Changes

### Old Docker Usage:
```bash
# Build
docker build -t clone-voice .

# Run
docker run -p 5000:5000 clone-voice
```

### New Docker Usage:
```bash
# Using docker-compose (recommended)
docker-compose up -d

# Or using docker directly
docker build -f docker/Dockerfile -t clone-voice .
docker run -p 5000:5000 clone-voice
```

### Docker Compose Paths:
```yaml
# Old paths in volumes:
- ./web_interface/uploads:/app/web_interface/uploads
- ./samples:/app/samples:ro

# New paths in volumes:
- ./data/uploads:/app/data/uploads
- ./data/samples:/app/data/samples:ro
```

---

## 🚀 Running the Application

### Old Way:
```bash
python web_interface/app.py
```

### New Ways:

**Method 1: Direct execution**
```bash
python main.py
```

**Method 2: Module execution**
```bash
python -m src.api.app
```

**Method 3: Installed package**
```bash
pip install -e .
clone-voice
```

**Method 4: Docker**
```bash
docker-compose up -d
```

---

## 📝 Code Examples

### Example 1: Creating TTS Instance

**Old:**
```python
from neuttsair.neutts import NeuTTSAir

tts = NeuTTSAir(
    backbone_repo="neuphonic/neutts-air",
    backbone_device="cpu"
)
```

**New:**
```python
from src.tts.engine import NeuTTSAir
from src.config.settings import get_config

config = get_config()
tts = NeuTTSAir(
    backbone_repo=config.TTS_BACKBONE_REPO,
    backbone_device=config.TTS_BACKBONE_DEVICE
)
```

### Example 2: Synthesizing Speech

**Old:**
```python
# Everything in one place
wav = tts.infer(text, ref_codes, ref_text)
```

**New:**
```python
# Using the service layer
from src.services.tts_service import get_tts_service
from src.models.synthesis_request import SynthesisRequest

request = SynthesisRequest(
    input_text=text,
    ref_text=ref_text,
    ref_audio_path=ref_path,
    session_id=session_id
)

tts_service = get_tts_service(session_manager, output_folder)
result = tts_service.synthesize(request)
```

### Example 3: Flask App Creation

**Old:**
```python
from web_interface.app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**New:**
```python
from src.api.app import create_app

app = create_app(env='development')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

## 🔍 Where Did It Go?

Quick reference for finding moved functionality:

| Looking for... | Check... |
|----------------|----------|
| Flask routes | `src/api/routes/` |
| TTS functionality | `src/tts/` |
| Business logic | `src/services/` |
| Configuration | `src/config/` |
| Utilities | `src/utils/` |
| Data models | `src/models/` |
| Templates | `templates/` |
| Static files | `src/api/static/` |
| Sample data | `data/samples/` |
| Docker files | `docker/` |
| Documentation | `docs/` |
| Scripts | `scripts/` |
| Tests | `tests/` |

---

## ⚠️ Breaking Changes

1. **Import paths changed** - Update all imports to new `src.*` structure
2. **File locations changed** - Update any hardcoded file paths
3. **Configuration required** - Must use `get_config()` instead of hardcoded values
4. **Docker paths changed** - Update volume mounts in docker-compose
5. **Entry point changed** - Use `main.py` instead of `web_interface/app.py`

---

## 🆘 Troubleshooting

### Import Errors
**Problem:** `ModuleNotFoundError: No module named 'src'`
**Solution:** Ensure you're running from project root and `PYTHONPATH` includes `src/`

### Path Errors
**Problem:** `FileNotFoundError: samples not found`
**Solution:** Samples moved to `data/samples/` - update paths

### Docker Build Errors
**Problem:** `COPY failed: no source files were specified`
**Solution:** Use `docker build -f docker/Dockerfile .` from project root

### Configuration Errors
**Problem:** `SECRET_KEY must be set in production`
**Solution:** Create `.env` file with `SECRET_KEY=your-secret-key`

---

## ✅ Migration Checklist

- [ ] Update import statements to new `src.*` paths
- [ ] Move custom code to appropriate new locations
- [ ] Update configuration to use `get_config()`
- [ ] Update file paths (samples, uploads, outputs)
- [ ] Update Docker configuration if customized
- [ ] Test application with new structure
- [ ] Update any external scripts or tools
- [ ] Update documentation for your team
- [ ] Run tests to verify functionality
- [ ] Deploy and verify in staging environment

---

**Need help?** Check `REFACTORING_SUMMARY.md` for more details or open an issue on GitHub.
