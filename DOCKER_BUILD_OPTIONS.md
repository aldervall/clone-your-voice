# Docker Build Options

NeuTTS-Air Web offers two Docker build options to suit different needs:

## 🚀 Full Build (Recommended)

**Includes:** llama-cpp-python + onnxruntime

**Best for:**
- Production deployments
- Users wanting GGUF model support (Q4, Q8)
- Better inference performance
- Lower memory usage with quantized models

**Build time:** 5-10 minutes (compiles llama-cpp-python)
**Image size:** ~4-5 GB

### Usage:
```bash
# Build and start
./docker-run.sh

# Or with docker-compose directly
docker-compose build
docker-compose up -d
```

**Supported models:**
- ✅ neuphonic/neutts-air (standard)
- ✅ neuphonic/neutts-air-q4-gguf (fastest)
- ✅ neuphonic/neutts-air-q8-gguf (balanced)

---

## 🪶 Lite Build

**Includes:** Core dependencies only (no llama-cpp-python)

**Best for:**
- Quick testing and development
- Users only using standard models
- Faster build times
- Smaller image size

**Build time:** 2-3 minutes
**Image size:** ~3-4 GB

### Usage:
```bash
# Build and start lite version
./docker-run.sh --lite

# Or with docker-compose directly
docker-compose -f docker-compose.lite.yml build
docker-compose -f docker-compose.lite.yml up -d
```

**Supported models:**
- ✅ neuphonic/neutts-air (standard only)
- ❌ GGUF models not supported

---

## 📊 Comparison

| Feature | Full Build | Lite Build |
|---------|-----------|------------|
| Build Time | 5-10 min | 2-3 min |
| Image Size | ~4-5 GB | ~3-4 GB |
| Standard Models | ✅ Yes | ✅ Yes |
| GGUF Models (Q4/Q8) | ✅ Yes | ❌ No |
| llama-cpp-python | ✅ Yes | ❌ No |
| onnxruntime | ✅ Yes | ❌ No |
| OpenBLAS | ✅ Yes | ❌ No |

---

## 🛠️ Technical Details

### Full Build (Dockerfile)

```dockerfile
# Includes build tools
- build-essential
- cmake
- libopenblas-dev
- pkg-config

# Python packages
- llama-cpp-python (with OpenBLAS)
- onnxruntime
- flask
- all requirements.txt
```

**Compilation flags:**
```bash
CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS"
```

### Lite Build (Dockerfile.lite)

```dockerfile
# Minimal dependencies
- espeak
- libsndfile1
- git
- curl

# Python packages
- flask
- all requirements.txt (no optional deps)
```

---

## 🎯 Which Should You Choose?

### Choose Full Build if:
- ✅ You want the best performance
- ✅ You plan to use GGUF models
- ✅ You have 10 minutes for initial build
- ✅ You're deploying to production

### Choose Lite Build if:
- ✅ You're just testing the interface
- ✅ You only use standard models
- ✅ You want faster builds
- ✅ You're developing locally

---

## 📝 Local Development (Python)

For local development without Docker:

```bash
# Core dependencies
pip install -r requirements.txt
pip install flask

# Optional: Add llama-cpp-python
pip install -r requirements-optional.txt

# Or manually
pip install llama-cpp-python onnxruntime
```

---

## 🔄 Switching Between Builds

```bash
# Stop current container
./docker-run.sh stop

# Clean up (optional)
./docker-run.sh clean

# Start with different build
./docker-run.sh        # Full build
./docker-run.sh --lite # Lite build
```

---

## 🐛 Troubleshooting

### Full build fails or takes too long

**Solution:** Use lite build instead
```bash
./docker-run.sh --lite
```

### Out of disk space

**Solution:**
1. Use lite build (smaller image)
2. Clean unused Docker images:
```bash
docker system prune -a
```

### llama-cpp-python compilation errors

**Possible causes:**
- Insufficient RAM during build (needs ~2GB)
- Missing build tools

**Solution:**
1. Try lite build
2. Or install llama-cpp-python locally after container runs

---

## 📦 Pre-built Images (Future)

We plan to provide pre-built images on Docker Hub to avoid compilation:

```bash
# Pull pre-built image (coming soon)
docker pull aldervall/neutts-air-web:latest
docker pull aldervall/neutts-air-web:lite
```

---

## 💡 Tips

1. **First time users:** Start with `./docker-run.sh --lite` for quick testing
2. **Production:** Use full build `./docker-run.sh` for best performance
3. **Development:** Use Python directly (faster iteration)
4. **CI/CD:** Use lite build for faster pipeline execution

---

## 🆘 Support

If you encounter build issues:

1. Check Docker and docker-compose versions
2. Ensure adequate disk space (10GB+ recommended)
3. Try lite build first
4. Check GitHub issues: https://github.com/aldervall/neutts-air-web/issues
