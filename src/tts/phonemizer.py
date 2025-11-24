"""
Text to Phoneme Conversion
Handles phonemization of text for TTS
"""
from phonemizer.backend import EspeakBackend
from src.config.logging_config import get_logger

logger = get_logger(__name__)


class Phonemizer:
    """Text to phoneme converter using espeak backend"""

    def __init__(self, language: str = "en-us", preserve_punctuation: bool = True, with_stress: bool = True):
        """
        Initialize phonemizer

        Args:
            language: Language code for phonemization
            preserve_punctuation: Whether to preserve punctuation
            with_stress: Whether to include stress markers
        """
        logger.info(f"Loading phonemizer for language: {language}")
        self.backend = EspeakBackend(
            language=language,
            preserve_punctuation=preserve_punctuation,
            with_stress=with_stress
        )

    def phonemize(self, text: str) -> str:
        """
        Convert text to phonemes

        Args:
            text: Input text

        Returns:
            Phonemized text
        """
        phones = self.backend.phonemize([text])
        phones = phones[0].split()
        phones = " ".join(phones)
        logger.debug(f"Phonemized: '{text[:50]}...' -> '{phones[:50]}...'")
        return phones

    def phonemize_batch(self, texts: list[str]) -> list[str]:
        """
        Convert multiple texts to phonemes

        Args:
            texts: List of input texts

        Returns:
            List of phonemized texts
        """
        results = []
        for text in texts:
            results.append(self.phonemize(text))
        return results
