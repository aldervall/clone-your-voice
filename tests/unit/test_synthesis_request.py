
import pytest
from pathlib import Path
from src.models.synthesis_request import SynthesisRequest

def test_synthesis_request_validation():
    # Valid request
    req = SynthesisRequest(
        input_text="Hello",
        ref_text="Reference",
        ref_audio_path=Path("dummy.wav"),
        language="en-us"
    )
    # Mock existence of file
    Path("dummy.wav").touch()
    
    is_valid, error = req.validate()
    assert is_valid
    assert error is None
    
    # Invalid request (missing input text)
    req.input_text = ""
    is_valid, error = req.validate()
    assert not is_valid
    assert error == "Input text is required"
    
    # Cleanup
    Path("dummy.wav").unlink()

def test_synthesis_request_default_language():
    req = SynthesisRequest(
        input_text="Hello",
        ref_text="Reference",
        ref_audio_path=Path("dummy.wav")
    )
    assert req.language == "en-us"
