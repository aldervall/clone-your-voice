"""
Synthesis Response Models
Data models for TTS synthesis responses
"""
from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class SynthesisProgress:
    """Progress update for synthesis operation"""

    step: int
    message: str
    progress: int  # 0-100
    session_id: str


@dataclass
class SynthesisResult:
    """Result of synthesis operation"""

    success: bool
    session_id: str

    # Success fields
    output_file: Optional[str] = None
    output_path: Optional[Path] = None
    chunks_processed: int = 0
    duration_seconds: Optional[float] = None

    # Error fields
    error_message: Optional[str] = None

    @classmethod
    def success_result(
        cls,
        session_id: str,
        output_file: str,
        output_path: Path,
        chunks_processed: int = 1,
        duration_seconds: Optional[float] = None
    ):
        """Create a successful result"""
        return cls(
            success=True,
            session_id=session_id,
            output_file=output_file,
            output_path=output_path,
            chunks_processed=chunks_processed,
            duration_seconds=duration_seconds
        )

    @classmethod
    def error_result(cls, session_id: str, error_message: str):
        """Create an error result"""
        return cls(
            success=False,
            session_id=session_id,
            error_message=error_message
        )

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        data = {
            "success": self.success,
            "session_id": self.session_id,
        }

        if self.success:
            data.update({
                "output_file": self.output_file,
                "chunks_processed": self.chunks_processed,
            })
            if self.duration_seconds is not None:
                data["duration_seconds"] = self.duration_seconds
        else:
            data["error"] = self.error_message

        return data
