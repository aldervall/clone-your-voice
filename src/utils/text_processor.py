"""
Text Processing Utilities
Handles text chunking and preprocessing for TTS
"""
import re
from typing import List
from src.config.logging_config import get_logger

logger = get_logger(__name__)


def split_text_into_chunks(text: str, max_tokens: int = 1200) -> List[str]:
    """
    Split text into chunks that fit within the model's context window.
    Uses sentence boundaries for natural splits.

    Args:
        text: Input text to split
        max_tokens: Maximum tokens per chunk (default 1200 to leave large margin)

    Returns:
        List of text chunks

    Note:
        Uses conservative character-to-token estimation for safety
    """
    # Very conservative estimate for tokenization
    # The model counts tokens including prompt, so we need a large safety margin
    # Rough estimate: 1 token ≈ 1 character (very conservative)
    max_chars = max_tokens

    # If text is short enough, return as is
    if len(text) <= max_chars:
        logger.debug(f"Text length {len(text)} chars - no chunking needed")
        return [text]

    # Split into sentences (handle multiple languages)
    sentences = re.split(r'(?<=[.!?।॥。！？])\s+', text)
    logger.debug(f"Split text into {len(sentences)} sentences")

    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence)

        # If single sentence is too long, split it further
        if sentence_length > max_chars:
            # If we have accumulated sentences, save them first
            if current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_length = 0

            # Split long sentence by commas or clauses
            parts = re.split(r'([,;:])\s*', sentence)
            temp_part = []
            temp_length = 0

            for part in parts:
                part_length = len(part)
                if temp_length + part_length > max_chars and temp_part:
                    chunks.append(''.join(temp_part))
                    temp_part = [part]
                    temp_length = part_length
                else:
                    temp_part.append(part)
                    temp_length += part_length

            if temp_part:
                chunks.append(''.join(temp_part))

        # If adding this sentence exceeds limit, start new chunk
        elif current_length + sentence_length > max_chars:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length

        # Add sentence to current chunk
        else:
            current_chunk.append(sentence)
            current_length += sentence_length + 1  # +1 for space

    # Add remaining chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    logger.info(f"Split text ({len(text)} chars) into {len(chunks)} chunks")
    for i, chunk in enumerate(chunks):
        logger.debug(f"  Chunk {i+1}: {len(chunk)} characters")

    return chunks


def clean_text(text: str) -> str:
    """
    Clean and normalize text for TTS processing

    Args:
        text: Input text to clean

    Returns:
        Cleaned text
    """
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text


def validate_text_length(text: str, max_length: int = 10000) -> bool:
    """
    Validate text length is within acceptable bounds

    Args:
        text: Text to validate
        max_length: Maximum allowed length

    Returns:
        True if valid, False otherwise
    """
    return 0 < len(text) <= max_length
