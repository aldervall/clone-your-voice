# Handover: Hosting Configuration & Audio Format Fixes

## Date: November 24, 2025

## Summary
Addressed issues related to hosting the application on an external domain (`https://clonevoice.aldervall.se`) and fixed a critical crash when processing browser-recorded audio.

## Changes

### 1. External Hosting Support (`BASE_URL`)
To support hosting the frontend behind a reverse proxy or on a specific domain, we introduced the `BASE_URL` configuration.
- **Backend**:
    - `src/config/settings.py`: Reads `BASE_URL` from environment variables.
    - `src/api/routes/main.py`: Passes `BASE_URL` to the frontend template.
- **Frontend**:
    - `templates/index.html`: Added a `getUrl()` helper function that prepends `BASE_URL` (if set) to all API requests (`fetch`, `EventSource`, audio playback, and downloads).
- **Configuration**:
    - `.env.example`: Added `BASE_URL` field.
    - Documentation (`docs/QUICKSTART.md`, `docs/DOCKER_DEPLOYMENT.md`) updated with usage instructions.

### 2. Audio Format Compatibility (WebM/FFmpeg)
Fixed `soundfile.LibsndfileError` caused by browsers recording in web-native formats (like WebM or Ogg) wrapped in WAV containers, which `libsndfile` could not read.
- **Docker**:
    - Updated `docker/Dockerfile` to install `ffmpeg`. This allows the backend to transparently handle `webm`, `ogg`, and other formats via `audioread`.
- **Validation**:
    - Updated `src/utils/validators.py` to explicitly allow `.webm` file extensions.

## Verification
- **Hosting**: The application can now be configured with `BASE_URL=https://your-domain.com` in the `.env` file, ensuring client-side requests resolve correctly.
- **Recording**: Browser recordings (which often default to WebM/Opus) will now be processed correctly by the backend without crashing.

## Required Actions
**You must rebuild the Docker container** for the `ffmpeg` installation to take effect:

```bash
docker-compose down
docker-compose up -d --build
```
