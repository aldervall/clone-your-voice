# Handover: Multilingual Support Implementation

## Date: November 24, 2025

## Summary
Implemented multilingual support for the Clone Your Voice application. The system now supports selecting a language for recording and synthesis, using the `neuphonic/neutts-air` model's capabilities (backed by `espeak` for phonemization).

## Changes

### Frontend (`templates/index.html`)
- Added a language selection dropdown with options: English (US), Spanish, French, German, Italian, Portuguese (Brazil).
- Updated the prompt generation logic to provide language-specific sample text for recording.
- Updated the `generateSpeech` function to pass the selected `language` parameter to the backend API.

### Backend (`src/`)
- **API (`src/api/routes/synthesis.py`)**: 
    - Updated `/synthesize` endpoint to accept and validate the `language` parameter.
- **Models (`src/models/synthesis_request.py`)**: 
    - Added `language` field to `SynthesisRequest` (default: "en-us").
- **Service (`src/services/tts_service.py`)**: 
    - Passed the `language` parameter from the request to the TTS engine.
- **TTS Engine (`src/tts/engine.py`)**: 
    - Refactored `NeuTTSAir` to manage a cache of `Phonemizer` instances (`self.phonemizers`).
    - Updated `infer` and `infer_stream` methods to accept a `language` argument.
    - Implemented lazy loading for phonemizers to minimize resource usage (only load what's needed).

### Testing
- Added `tests/unit/test_synthesis_request.py`: Verifies request model validation including the new language field.
- Added `tests/unit/test_tts_engine.py`: Verifies that the TTS engine correctly manages phonemizer instances (creation and caching) based on the requested language.

## Dependencies
- The implementation relies on `espeak` (or `espeak-ng`) being available in the environment.
- The `Dockerfile` already includes `espeak`, so no Docker changes were strictly necessary for dependencies, but verify `espeak` is installed if running locally.

## Next Steps / Recommendations
- **Model Support**: While `neutts-air` works with these languages, verify the quality of the specific model checkpoint being used. Some languages might perform better with specific fine-tunes if available in the future.
- **UI Improvements**: The language selector is basic. Future iterations could add flags or better styling.
- **Error Handling**: Currently defaults to "en-us" if issues arise; more robust error handling for unsupported language codes could be added.
