"""
General Helper Utilities
Miscellaneous helper functions
"""
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from src.config.logging_config import get_logger

logger = get_logger(__name__)


def generate_timestamp_filename(prefix: str = "", extension: str = "wav") -> str:
    """
    Generate a filename with timestamp

    Args:
        prefix: Optional prefix for the filename
        extension: File extension (without dot)

    Returns:
        Filename string
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if prefix:
        return f"{prefix}_{timestamp}.{extension}"
    return f"{timestamp}.{extension}"


def generate_session_id() -> str:
    """
    Generate a unique session ID

    Returns:
        Session ID string
    """
    return datetime.now().strftime('%Y%m%d_%H%M%S_%f')


def get_file_info(file_path: Path) -> Dict[str, Any]:
    """
    Get information about a file

    Args:
        file_path: Path to the file

    Returns:
        Dictionary with file information
    """
    if not file_path.exists():
        return {"exists": False}

    stat = file_path.stat()
    return {
        "exists": True,
        "size_bytes": stat.st_size,
        "size_mb": stat.st_size / (1024 * 1024),
        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "extension": file_path.suffix.lstrip('.'),
        "name": file_path.name,
    }


def cleanup_old_files(directory: Path, max_age_hours: int = 24) -> int:
    """
    Clean up old files from a directory

    Args:
        directory: Directory to clean
        max_age_hours: Maximum age of files to keep (in hours)

    Returns:
        Number of files deleted
    """
    if not directory.exists():
        return 0

    from datetime import timedelta
    cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
    deleted_count = 0

    try:
        for file_path in directory.iterdir():
            if file_path.is_file():
                file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_mtime < cutoff_time:
                    logger.debug(f"Deleting old file: {file_path}")
                    file_path.unlink()
                    deleted_count += 1
    except Exception as e:
        logger.error(f"Error cleaning up old files: {e}")

    if deleted_count > 0:
        logger.info(f"Cleaned up {deleted_count} old files from {directory}")

    return deleted_count


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string (e.g., "1m 30s", "45s")
    """
    if seconds < 60:
        return f"{seconds:.0f}s"

    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)

    if minutes < 60:
        return f"{minutes}m {remaining_seconds}s"

    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours}h {remaining_minutes}m"


def get_sample_files(samples_dir: Path) -> List[Dict[str, Any]]:
    """
    Get list of available sample files

    Args:
        samples_dir: Directory containing samples

    Returns:
        List of sample dictionaries with name, wav path, and txt content
    """
    samples = []

    if not samples_dir.exists():
        logger.warning(f"Samples directory does not exist: {samples_dir}")
        return samples

    # Find all wav files
    for wav_file in samples_dir.glob('*.wav'):
        name = wav_file.stem
        txt_file = samples_dir / f"{name}.txt"

        # Read text content if available
        txt_content = None
        if txt_file.exists():
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    txt_content = f.read().strip()
            except Exception as e:
                logger.error(f"Error reading {txt_file}: {e}")

        samples.append({
            'name': name,
            'wav': str(wav_file),
            'txt': txt_content
        })

    logger.debug(f"Found {len(samples)} sample files")
    return samples
