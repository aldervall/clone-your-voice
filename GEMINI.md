# Project: Clone Your Voice 2.0 (Refactored)

## Project Overview

**Clone Your Voice 2.0** is an AI-powered voice cloning application designed for simplicity, efficiency, and privacy. It allows users to:
1.  **Record Voice:** Record a 10-second sample directly in the browser.
2.  **Clone Voice:** Uses the **NeuTTS-Air** model (Qwen 0.5B backbone) to create a digital voice replica.
3.  **Generate Speech:** Synthesize new speech from text using the cloned voice.

**Key Characteristics:**
*   **Optimized:** Runs on CPU (no GPU required), uses a minimized Docker image (~1.5GB).
*   **Privacy-Focused:** Runs locally or in a self-hosted Docker container.
*   **Modern Stack:** Python 3.11, Flask, Vanilla JS, Docker.

## Technical Architecture

### Directory Structure
*   `src/`: Main application source code.
    *   `api/`: Flask application, routes (`synthesis`, `media`), and middleware.
    *   `services/`: Business logic for TTS orchestration (`tts_service.py`), session management, and file handling.
    *   `tts/`: Core TTS engine wrapper, handling inference, encoding/decoding (NeuCodec), and phonemization.
    *   `config/`: Configuration settings (`settings.py`) and logging setup.
    *   `models/`: Pydantic models for request/response validation.
*   `data/`: Persistent storage for samples, uploads (recordings), and outputs (synthesized audio).
*   `docker/`: Docker build files.
*   `scripts/`: Utility scripts (e.g., `build_and_run.sh`).

### Key Technologies
*   **Backend:** Python 3.11, Flask.
*   **AI/ML:** PyTorch (CPU), NeuTTS-Air, NeuCodec, Phonenmizer.
*   **Containerization:** Docker, Docker Compose.
*   **Frontend:** HTML5, JavaScript (No complex framework).

## Building and Running

### Using Docker (Recommended)
The project is optimized for Docker.
```bash
docker-compose up -d --build
```
Access the UI at `http://localhost:5000`.

### Local Development
1.  **Setup:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
2.  **Run:**
    ```bash
    python3 main.py
    ```

### Configuration
*   **Environment Variables:** Managed via `.env` file (see `.env.example`).
    *   `FLASK_ENV`: development/production
    *   `TTS_BACKBONE_DEVICE`: cpu (default)
*   **Settings Code:** `src/config/settings.py`

## Development Conventions

*   **Code Style:** Follows PEP 8. formatted with `black`.
*   **Type Hinting:** Uses Python type hints; validated with `mypy`.
*   **Testing:** `pytest` is used for testing (located in `tests/`).
*   **Documentation:** kept in `docs/` and `README.md`.

## Current Status
*   **Refactored:** The project has recently undergone a major refactor to clean up the architecture, remove unused files, and optimize the Docker build.
*   **Operational:** The codebase is ready for deployment or local testing.
