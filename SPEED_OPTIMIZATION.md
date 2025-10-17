# 🚀 Speed Optimization Guide

Get maximum performance from Clone My Voice 2.0!

## Quick Wins

### 1. Remove Resource Limits ✅ DONE!

The docker-compose.yml now has NO resource limits. Your container can use all available CPU and RAM for maximum speed!

### 2. Use BuildKit for Faster Builds

```bash
# Fast build with parallel layer processing
DOCKER_BUILDKIT=1 docker compose build

# Or use the provided script
./BUILD_AND_RUN.sh
```

### 3. Optimize Your System

**For Linux/WSL2:**
```bash
# Check current CPU governor
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# Set to performance mode (requires sudo)
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

**For Docker Desktop:**
- Settings → Resources → Increase CPU cores to maximum
- Settings → Resources → Increase RAM to 8GB or more

## Performance Tuning

### Environment Variables for Speed

Add these to docker-compose.yml:

```yaml
environment:
  - FLASK_ENV=production
  - PYTHONUNBUFFERED=1
  - OMP_NUM_THREADS=8          # OpenMP threads (match your CPU cores)
  - MKL_NUM_THREADS=8          # Intel MKL threads
  - OPENBLAS_NUM_THREADS=8     # OpenBLAS threads
  - NUMEXPR_NUM_THREADS=8      # NumExpr threads
```

### PyTorch Performance

Create `clone-my-voice-2.0/web_interface/speed_config.py`:

```python
import torch

# Enable CPU optimizations
torch.set_num_threads(8)  # Match your CPU cores
torch.set_num_interop_threads(2)

# Enable oneDNN (faster on Intel CPUs)
torch.backends.mkldnn.enabled = True

# Disable gradient computation (inference only)
torch.set_grad_enabled(False)
```

Then import in `app.py`:
```python
import speed_config  # Add at top of web_interface/app.py
```

## Benchmarking

### Test Inference Speed

```bash
# Enter container
docker exec -it clone-my-voice-2.0 bash

# Time a simple inference
time python -c "
from neuttsair.neutts import NeuTTSAir
tts = NeuTTSAir(backbone_repo='neuphonic/neutts-air')
ref_codes = tts.encode_reference('samples/sample1.wav')
wav = tts.infer('Hello world', ref_codes, 'reference text')
"
```

### Monitor Resource Usage

```bash
# Watch container stats in real-time
docker stats clone-my-voice-2.0

# Or use htop inside container
docker exec -it clone-my-voice-2.0 apt-get update && apt-get install -y htop
docker exec -it clone-my-voice-2.0 htop
```

## Expected Performance

### Inference Times (varies by CPU)

**Short text (10-20 words):**
- Fast CPU (8+ cores): 2-4 seconds
- Medium CPU (4 cores): 5-8 seconds
- Slow CPU (2 cores): 10-15 seconds

**Long text (100+ words):**
- Fast CPU: 10-20 seconds
- Medium CPU: 20-40 seconds
- Slow CPU: 40-60 seconds

### First Run is Slower

The first inference loads models into memory:
- First run: +10-30 seconds (model loading)
- Subsequent runs: Fast (cached in memory)

## Advanced: Use GGUF Quantized Models (Fastest!)

For maximum speed, use quantized models:

Edit `web_interface/app.py` line 46:

```python
# Before (standard model)
tts_instance = NeuTTSAir(
    backbone_repo="neuphonic/neutts-air",
    backbone_device="cpu",
)

# After (quantized model - FASTER)
tts_instance = NeuTTSAir(
    backbone_repo="neuphonic/neutts-air-0.5b-gguf",  # Quantized version
    backbone_device="cpu",
)
```

**Note:** Requires `llama-cpp-python` to be installed (add to requirements.txt)

## Bottleneck Analysis

### Where Time is Spent

1. **Model Loading** (first time only): 10-20 sec
2. **Text Phonemization**: <1 sec
3. **Reference Encoding**: 1-2 sec
4. **Token Generation**: 5-30 sec ⚠️ BOTTLENECK
5. **Audio Decoding**: 1-2 sec
6. **Watermarking**: <1 sec

**The bottleneck is token generation** - this is CPU-bound and depends on:
- CPU speed (GHz)
- Number of cores
- CPU architecture (newer = faster)
- Text length

## Speed vs Quality Tradeoffs

You can trade quality for speed by modifying inference parameters in `neuttsair/neutts.py`:

```python
# Line 261-270 (in _infer_torch method)
output_tokens = self.backbone.generate(
    prompt_tensor,
    max_length=self.max_context,
    eos_token_id=speech_end_id,
    do_sample=True,
    temperature=1.0,        # Lower = faster but more robotic (try 0.7)
    top_k=50,               # Lower = faster (try 20)
    use_cache=True,
    min_new_tokens=50,      # Lower = faster for short text (try 25)
)
```

## Caching Strategy

For production, implement caching:

1. **Cache encoded references** - Same voice = reuse encoding
2. **Cache common phrases** - Repeated text = instant response
3. **Pre-warm models** - Load on startup, not first request

Example cache implementation:

```python
# Add to web_interface/app.py
from functools import lru_cache

@lru_cache(maxsize=10)
def encode_reference_cached(ref_audio_path):
    return get_tts().encode_reference(ref_audio_path)
```

## Monitoring

Track these metrics:

```bash
# CPU usage per core
docker exec clone-my-voice-2.0 top -bn1 | grep "Cpu(s)"

# Memory usage
docker exec clone-my-voice-2.0 free -h

# Check for swapping (BAD for speed)
docker exec clone-my-voice-2.0 vmstat 1

# Disk I/O (should be minimal)
docker exec clone-my-voice-2.0 iostat -x 1
```

## Troubleshooting Slow Performance

### Issue: Very slow even with fast CPU

**Check:**
```bash
# Is CPU throttling?
cat /proc/cpuinfo | grep MHz

# Is system swapping? (should be 0)
free -h

# Are other containers hogging resources?
docker stats
```

**Fix:**
- Close other applications
- Ensure no resource limits in docker-compose.yml ✅
- Check CPU temperature (throttling?)
- Disable power saving modes

### Issue: Out of memory crashes

**Solution:**
- Process shorter text chunks
- Close other applications
- Add swap space (slower but prevents crashes)

## Summary

✅ **Already Optimized:**
- Multi-stage Docker build
- CPU-only PyTorch
- No resource limits
- Efficient layer caching

🚀 **To Optimize Further:**
1. Use BuildKit for builds: `DOCKER_BUILDKIT=1 docker compose build`
2. Add PyTorch threading config (speed_config.py)
3. Use GGUF quantized models
4. Implement caching for repeated requests
5. Set CPU governor to "performance" mode

📊 **Monitor:**
```bash
# Real-time stats
docker stats clone-my-voice-2.0

# Detailed logs
docker compose logs -f
```
