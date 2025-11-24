# Handover: Torchaudio CPU Fix

**Date:** November 24, 2025
**Topic:** Fix for `OSError: libtorch_cuda.so` in Docker environment
**Status:** ✅ Resolved

---

## 🚨 Issue Description

When running the application via Docker, the container would crash with the following error:

```
OSError: libtorch_cuda.so: cannot open shared object file: No such file or directory
```

This error occurred despite the project being configured for CPU-only usage. It was triggered by `torchaudio` attempting to load CUDA libraries that are not present in the CPU-only base image.

## 🔍 Root Cause

The dependency `resemble-perth` (used for watermarking) has a dependency on `torchaudio`. While we explicitly installed the CPU-only version of `torch` in the `Dockerfile`, we did not explicitly install the CPU-only version of `torchaudio`.

As a result, `pip` installed the default version of `torchaudio` from PyPI, which is built with CUDA support and looks for `libtorch_cuda.so`.

## 🛠️ Resolution

We have explicitly pinned `torchaudio==2.8.0` to match the PyTorch version and ensured it is installed from the CPU-only PyTorch index in the Docker build process.

### Changes Made

1.  **`requirements.txt`**: Added `torchaudio==2.8.0` to explicitly declare the dependency and version lock.
2.  **`docker/Dockerfile`**: Updated the `pip install` command to include `torchaudio==2.8.0` alongside `torch` when installing from the `--index-url https://download.pytorch.org/whl/cpu`.

**Modified Dockerfile Command:**
```dockerfile
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    torch==2.8.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir flask
```

## 🔄 Verification

To apply this fix, you must rebuild the Docker image:

```bash
docker-compose up -d --build
```

The application should now start successfully without looking for CUDA libraries.

## 📂 Files Modified

*   `requirements.txt`
*   `docker/Dockerfile`
