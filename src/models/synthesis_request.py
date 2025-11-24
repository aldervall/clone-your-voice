"""
Synthesis Request Models
Data models for TTS synthesis requests
"""
from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class SynthesisRequest:
    """Request for text-to-speech synthesis"""

    # Input text to synthesize
    input_text: str

    # Reference audio and text
    ref_text: str
    ref_audio_path: Path

    # Optional model configuration
    backbone: str = "neuphonic/neutts-air"
    max_tokens: int = 1200

    # Session tracking
    session_id: Optional[str] = None

    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Validate the synthesis request

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.input_text or not self.input_text.strip():
            return False, "Input text is required"

        if not self.ref_text or not self.ref_text.strip():
            return False, "Reference text is required"

        if not self.ref_audio_path.exists():
            return False, f"Reference audio file not found: {self.ref_audio_path}"

        return True, None

    @property
    def is_valid(self) -> bool:
        """Check if request is valid"""
        valid, _ = self.validate()
        return valid
