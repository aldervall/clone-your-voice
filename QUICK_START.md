# NeuTTS-Air Quick Start Guide

Three ways to run the NeuTTS-Air web interface:

## 🐳 Option 1: Docker (Recommended for Production)

```bash
# Quick start - build and run
./docker-run.sh

# Access at http://localhost:5000
```

**Pros:**
- ✅ Isolated environment
- ✅ Easy deployment
- ✅ Consistent across systems
- ✅ Auto-restart on failure
- ✅ Easy updates

**Cons:**
- ❌ Requires Docker installed
- ❌ First build takes ~5 minutes

See [DOCKER_README.md](DOCKER_README.md) for details.

---

## 🚀 Option 2: Direct Python (Development)

```bash
# Start the server
cd /home/amdvall/neutts-air/web_interface
./start.sh

# Or manually:
source ../.venv/bin/activate
python app.py
```

**Pros:**
- ✅ Instant startup
- ✅ Easy debugging
- ✅ Live code reload
- ✅ Direct access to files

**Cons:**
- ❌ Requires Python setup
- ❌ Dependencies must be installed
- ❌ Not isolated

---

## 📦 Option 3: Original CLI (No Web Interface)

```bash
cd /home/amdvall/neutts-air
source .venv/bin/activate

python -m examples.basic_example \
  --input_text "Hello, this is a test" \
  --ref_audio samples/niklas.wav \
  --ref_text samples/niklas.txt
```

**Pros:**
- ✅ Simple and direct
- ✅ Scriptable
- ✅ No web server needed

**Cons:**
- ❌ Command line only
- ❌ Less user-friendly
- ❌ No GUI

---

## 📊 Comparison

| Feature | Docker | Python | CLI |
|---------|--------|--------|-----|
| Ease of Use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Setup Time | 5-10 min | 2-3 min | 1 min |
| GUI | ✅ Yes | ✅ Yes | ❌ No |
| Production Ready | ✅ Yes | ⚠️ Maybe | ❌ No |
| Debugging | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 🎯 Which Should You Choose?

- **New users** → Use Docker (easiest)
- **Developers** → Use Python (most flexible)
- **Scripts/Automation** → Use CLI (most direct)
- **Production** → Use Docker (most reliable)

---

## 🔗 Available Voices

All methods can use these voices:

- **dave** - English male voice (default)
- **jo** - English female voice
- **niklas** - Your Swedish voice!

---

## ⚡ Quick Commands

### Docker
```bash
./docker-run.sh          # Start
./docker-run.sh logs     # View logs
./docker-run.sh stop     # Stop
```

### Python
```bash
cd web_interface && ./start.sh    # Start
Ctrl+C                             # Stop
```

### CLI
```bash
python -m examples.basic_example --input_text "..." --ref_audio samples/niklas.wav --ref_text samples/niklas.txt
```

---

## 📚 More Information

- Web Interface: [web_interface/README.md](web_interface/README.md)
- Docker Setup: [DOCKER_README.md](DOCKER_README.md)
- Project Info: [README.md](README.md)
