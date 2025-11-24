# 🚀 Quick Start Guide

Get your Clone Your Voice application running in minutes!

---

## ⚡ 3 Ways to Run

### Method 1: Docker (Recommended) 🐳

**Fastest way to get started - no Python setup required!**

```bash
# Start the application
docker-compose up -d

# Open your browser
open http://localhost:5000
```

**Useful Docker commands:**
```bash
# View logs
docker-compose logs -f

# Stop the application
docker-compose down

# Restart
docker-compose restart

# Rebuild after code changes
docker-compose build --no-cache
docker-compose up -d
```

---

### Method 2: Automated Script 🤖

**Easy setup with our build script:**

```bash
# Run locally (creates venv, installs deps, runs app)
./scripts/build_and_run.sh local

# Or run with Docker
./scripts/build_and_run.sh docker
```

---

### Method 3: Manual Setup 💻

**Full control over your environment:**

#### Step 1: Create Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

#### Step 2: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

#### Step 3: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your preferences (optional for development)
nano .env
```

#### Step 4: Run the Application

```bash
# Run directly
python3 main.py

# Or use the module
python -m src.api.app

# Or install and use the package
pip install -e .
clone-voice
```

---

## 🎯 How to Use

### 1. **Open the Interface**
Navigate to `http://localhost:5000` in your browser

### 2. **Record Your Voice**
- Click the microphone button
- Read the displayed prompt aloud for ~10 seconds
- Preview your recording

### 3. **Generate Speech**
- Type any text you want to hear in your voice
- Click "Generate Speech"
- Wait for processing (~10-30 seconds)

### 4. **Download & Share**
- Listen to your generated audio
- Download the file
- Generate more!

---

## 📁 Understanding the Structure

### Key Directories

```
clone-your-voice/
├── src/              # All application code
│   ├── api/          # Flask routes and middleware
│   ├── services/     # Business logic
│   ├── tts/          # TTS engine
│   ├── config/       # Settings
│   └── utils/        # Helpers
├── data/             # Your data
│   ├── samples/      # Demo voices
│   ├── uploads/      # Your recordings
│   └── outputs/      # Generated audio
└── main.py           # Entry point
```

### Key Files

- `main.py` - Application entry point
- `docker-compose.yml` - Docker configuration
- `.env` - Environment variables
- `requirements.txt` - Python dependencies

---

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Flask Environment
FLASK_ENV=development          # development, production, testing

# Server Configuration
HOST=0.0.0.0                   # Host to bind to
PORT=5000                      # Port to run on

# TTS Configuration
TTS_BACKBONE_REPO=neuphonic/neutts-air    # Model repository
TTS_BACKBONE_DEVICE=cpu                    # cpu or cuda
TTS_MAX_TOKENS=1200                        # Max tokens per chunk

# Logging
LOG_LEVEL=INFO                 # DEBUG, INFO, WARNING, ERROR
LOG_FILE=                      # Optional log file path
```

### Configuration Files

- `src/config/settings.py` - Main configuration classes
- `.env` - Environment-specific overrides (create from `.env.example`)

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Change port in .env
PORT=5001

# Or in docker-compose.yml
ports:
  - "5001:5000"
```

### Module Not Found Errors

```bash
# Ensure you're in the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Check PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Docker Build Issues

```bash
# Clean rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Missing Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt

# Install dev dependencies (for testing)
pip install -r requirements-dev.txt
```

### Data Directory Permissions

```bash
# Fix permissions
chmod -R 755 data/
```

---

## 📊 System Requirements

**Minimum:**
- Python 3.11+
- 2 GB RAM
- 5 GB disk space

**Recommended:**
- Python 3.11+
- 4 GB RAM
- 10 GB disk space

**Note:** No GPU required! Runs on CPU.

---

## 🎓 Development Workflow

### 1. Make Code Changes

Edit files in `src/` directory

### 2. Test Changes

```bash
# Start the app
python3 main.py
```

### 3. Format Code (Optional)

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Format code
black src/ tests/

# Check types
mypy src/

# Lint
flake8 src/ tests/
```

### 4. Run Tests (when implemented)

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src
```

---

## 🚢 Deployment

### Local Deployment

```bash
# Set environment
export FLASK_ENV=production

# Set secret key
export SECRET_KEY="your-super-secret-key"

# Run with gunicorn (install first: pip install gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 "src.api.app:create_app('production')"
```

### Docker Deployment

```bash
# Build production image
docker-compose build

# Run in production mode
FLASK_ENV=production docker-compose up -d

# Or edit docker-compose.yml to set production by default
```

---

## 📚 Next Steps

### Explore the Code
- Check out `src/api/routes/` for API endpoints
- Look at `src/services/` for business logic
- Review `src/config/settings.py` for configuration options

### Read the Documentation
- `README.md` - Full project overview
- `docs/` - Check the documentation folder

### Customize
- Add your own sample voices to `data/samples/`
- Customize templates in `templates/`
- Modify configuration in `src/config/`

### Contribute
- Write tests in `tests/`
- Add features to `src/`
- Submit pull requests

---

## 🆘 Getting Help

- **Issues:** [GitHub Issues](https://github.com/aldervall/clone-your-voice/issues)
- **Documentation:** Check the `docs/` directory

---

**You're all set! Start cloning voices! 🎙️**
