"""
File Manager Service
Handles file upload, storage, and retrieval
"""
from pathlib import Path
from typing import Optional, Tuple
from werkzeug.datastructures import FileStorage

from src.utils.validators import validate_audio_file, sanitize_filename
from src.utils.helpers import generate_timestamp_filename
from src.config.logging_config import get_logger

logger = get_logger(__name__)


class FileManager:
    """Manages file operations for the application"""

    def __init__(self, upload_folder: Path, output_folder: Path, samples_folder: Path):
        """
        Initialize file manager

        Args:
            upload_folder: Directory for uploaded files
            output_folder: Directory for generated outputs
            samples_folder: Directory for sample files
        """
        self.upload_folder = upload_folder
        self.output_folder = output_folder
        self.samples_folder = samples_folder

        # Ensure directories exist
        self.upload_folder.mkdir(parents=True, exist_ok=True)
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self.samples_folder.mkdir(parents=True, exist_ok=True)

    def save_uploaded_audio(
        self,
        file: FileStorage,
        prefix: str = "ref"
    ) -> Tuple[bool, Optional[Path], Optional[str]]:
        """
        Save uploaded audio file

        Args:
            file: Uploaded file from Flask request
            prefix: Filename prefix

        Returns:
            Tuple of (success, file_path, error_message)
        """
        # Validate file
        is_valid, error_msg = validate_audio_file(file)
        if not is_valid:
            return False, None, error_msg

        try:
            # Generate safe filename
            original_filename = sanitize_filename(file.filename)
            extension = Path(original_filename).suffix.lstrip('.') or 'wav'
            filename = generate_timestamp_filename(prefix=prefix, extension=extension)

            # Save file
            file_path = self.upload_folder / filename
            file.save(str(file_path))

            logger.info(f"Saved uploaded file: {filename} ({file_path.stat().st_size} bytes)")
            return True, file_path, None

        except Exception as e:
            logger.error(f"Error saving uploaded file: {e}")
            return False, None, f"Failed to save file: {str(e)}"

    def get_sample_path(self, sample_name: str) -> Optional[Path]:
        """
        Get path to sample audio file

        Args:
            sample_name: Name of sample (without extension)

        Returns:
            Path to sample WAV file or None if not found
        """
        sample_path = self.samples_folder / f"{sample_name}.wav"
        if sample_path.exists():
            return sample_path
        return None

    def get_sample_text(self, sample_name: str) -> Optional[str]:
        """
        Get text content for sample

        Args:
            sample_name: Name of sample (without extension)

        Returns:
            Text content or None if not found
        """
        text_path = self.samples_folder / f"{sample_name}.txt"
        if text_path.exists():
            try:
                with open(text_path, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            except Exception as e:
                logger.error(f"Error reading sample text {text_path}: {e}")
        return None

    def get_output_path(self, filename: str) -> Optional[Path]:
        """
        Get path to output file

        Args:
            filename: Output filename

        Returns:
            Path to output file or None if not found
        """
        # Sanitize filename to prevent path traversal
        safe_filename = sanitize_filename(filename)
        output_path = self.output_folder / safe_filename

        if output_path.exists() and output_path.parent == self.output_folder:
            return output_path
        return None

    def cleanup_old_uploads(self, max_age_hours: int = 24) -> int:
        """
        Clean up old uploaded files

        Args:
            max_age_hours: Maximum age in hours

        Returns:
            Number of files deleted
        """
        from src.utils.helpers import cleanup_old_files
        return cleanup_old_files(self.upload_folder, max_age_hours)

    def cleanup_old_outputs(self, max_age_hours: int = 24) -> int:
        """
        Clean up old output files

        Args:
            max_age_hours: Maximum age in hours

        Returns:
            Number of files deleted
        """
        from src.utils.helpers import cleanup_old_files
        return cleanup_old_files(self.output_folder, max_age_hours)


# Global file manager instance
_file_manager: Optional[FileManager] = None


def get_file_manager(
    upload_folder: Path,
    output_folder: Path,
    samples_folder: Path
) -> FileManager:
    """
    Get or create global file manager instance

    Args:
        upload_folder: Upload directory
        output_folder: Output directory
        samples_folder: Samples directory

    Returns:
        FileManager instance
    """
    global _file_manager
    if _file_manager is None:
        _file_manager = FileManager(upload_folder, output_folder, samples_folder)
    return _file_manager
