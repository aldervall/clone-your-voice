"""
Input Validation Utilities
Validates user inputs and file uploads
"""
from pathlib import Path
from typing import Optional, Tuple
from werkzeug.datastructures import FileStorage
from src.config.logging_config import get_logger

logger = get_logger(__name__)


class ValidationError(Exception):
    """Raised when validation fails"""
    pass


def validate_audio_file(
    file: FileStorage,
    max_size_mb: int = 50,
    allowed_extensions: Optional[set] = None
) -> Tuple[bool, Optional[str]]:
    """
    Validate uploaded audio file

    Args:
        file: Uploaded file from Flask request
        max_size_mb: Maximum file size in MB
        allowed_extensions: Set of allowed file extensions (e.g., {'wav', 'mp3'})

    Returns:
        Tuple of (is_valid, error_message)
    """
    if allowed_extensions is None:
        allowed_extensions = {'wav', 'mp3', 'flac', 'ogg'}

    # Check if file exists
    if not file or file.filename == '':
        return False, "No file provided"

    # Check file extension
    file_ext = Path(file.filename).suffix.lower().lstrip('.')
    if file_ext not in allowed_extensions:
        return False, f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"

    # Check file size (if we can determine it)
    try:
        file.seek(0, 2)  # Seek to end
        size_bytes = file.tell()
        file.seek(0)  # Reset to beginning

        max_size_bytes = max_size_mb * 1024 * 1024
        if size_bytes > max_size_bytes:
            size_mb = size_bytes / (1024 * 1024)
            return False, f"File too large ({size_mb:.1f}MB). Maximum: {max_size_mb}MB"

        logger.debug(f"Audio file validated: {file.filename} ({size_bytes} bytes)")
    except Exception as e:
        logger.warning(f"Could not determine file size: {e}")

    return True, None


def validate_text_input(
    text: str,
    min_length: int = 1,
    max_length: int = 10000,
    field_name: str = "Text"
) -> Tuple[bool, Optional[str]]:
    """
    Validate text input

    Args:
        text: Text to validate
        min_length: Minimum text length
        max_length: Maximum text length
        field_name: Name of field for error messages

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not text:
        return False, f"{field_name} is required"

    text = text.strip()

    if len(text) < min_length:
        return False, f"{field_name} must be at least {min_length} characters"

    if len(text) > max_length:
        return False, f"{field_name} must be at most {max_length} characters"

    return True, None


def validate_sample_name(
    sample_name: str,
    samples_dir: Path
) -> Tuple[bool, Optional[str]]:
    """
    Validate that a sample name exists

    Args:
        sample_name: Name of the sample (without extension)
        samples_dir: Directory containing samples

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not sample_name:
        return False, "Sample name is required"

    # Check for path traversal attempts
    if '..' in sample_name or '/' in sample_name or '\\' in sample_name:
        return False, "Invalid sample name"

    # Check if sample files exist
    wav_path = samples_dir / f"{sample_name}.wav"
    txt_path = samples_dir / f"{sample_name}.txt"

    if not wav_path.exists():
        return False, f"Sample not found: {sample_name}"

    if not txt_path.exists():
        logger.warning(f"Sample {sample_name} missing .txt file")

    return True, None


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal and other issues

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Remove path components
    filename = Path(filename).name

    # Remove or replace dangerous characters
    # Keep only alphanumeric, dash, underscore, and dot
    import re
    filename = re.sub(r'[^\w\-.]', '_', filename)

    # Ensure filename is not empty
    if not filename:
        filename = "file"

    return filename
