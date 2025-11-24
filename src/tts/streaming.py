"""
Streaming TTS Processing
Handles streaming inference for real-time generation
"""
import numpy as np
from typing import Generator
from src.tts.utils import linear_overlap_add
from src.config.logging_config import get_logger

logger = get_logger(__name__)


class StreamingProcessor:
    """Processes streaming TTS generation"""

    def __init__(
        self,
        decoder,
        watermarker,
        hop_length: int = 480,
        frames_per_chunk: int = 25,
        lookforward: int = 5,
        lookback: int = 50,
        overlap_frames: int = 1,
        sample_rate: int = 24000
    ):
        """
        Initialize streaming processor

        Args:
            decoder: Speech decoder instance
            watermarker: Audio watermarker instance
            hop_length: Hop length for codec frames
            frames_per_chunk: Number of frames per streaming chunk
            lookforward: Frames to look ahead
            lookback: Frames to look back
            overlap_frames: Overlap between chunks
            sample_rate: Audio sample rate
        """
        self.decoder = decoder
        self.watermarker = watermarker
        self.hop_length = hop_length
        self.frames_per_chunk = frames_per_chunk
        self.lookforward = lookforward
        self.lookback = lookback
        self.overlap_frames = overlap_frames
        self.sample_rate = sample_rate
        self.stride_samples = frames_per_chunk * hop_length

    def process_stream(
        self,
        token_generator: Generator[str, None, None],
        ref_codes: list[int]
    ) -> Generator[np.ndarray, None, None]:
        """
        Process streaming token generation

        Args:
            token_generator: Generator yielding speech tokens
            ref_codes: Reference audio codes

        Yields:
            Audio chunks as numpy arrays
        """
        audio_cache: list[np.ndarray] = []
        token_cache: list[str] = [f"<|speech_{idx}|>" for idx in ref_codes]
        n_decoded_samples: int = 0
        n_decoded_tokens: int = len(ref_codes)

        logger.info("Starting streaming TTS processing")

        for output_str in token_generator:
            token_cache.append(output_str)

            # Check if we have enough tokens for a chunk
            if len(token_cache[n_decoded_tokens:]) >= self.frames_per_chunk + self.lookforward:

                # Decode chunk
                tokens_start = max(
                    n_decoded_tokens
                    - self.lookback
                    - self.overlap_frames,
                    0
                )
                tokens_end = (
                    n_decoded_tokens
                    + self.frames_per_chunk
                    + self.lookforward
                    + self.overlap_frames
                )
                sample_start = (
                    n_decoded_tokens - tokens_start
                ) * self.hop_length
                sample_end = (
                    sample_start
                    + (self.frames_per_chunk + 2 * self.overlap_frames) * self.hop_length
                )

                # Get current codes and decode
                curr_codes = token_cache[tokens_start:tokens_end]
                recon = self.decoder.decode("".join(curr_codes))
                recon = self.watermarker.apply_watermark(recon, sample_rate=self.sample_rate)
                recon = recon[sample_start:sample_end]
                audio_cache.append(recon)

                # Postprocess with overlap-add
                processed_recon = linear_overlap_add(
                    audio_cache, stride=self.stride_samples
                )
                new_samples_end = len(audio_cache) * self.stride_samples
                processed_recon = processed_recon[
                    n_decoded_samples:new_samples_end
                ]
                n_decoded_samples = new_samples_end
                n_decoded_tokens += self.frames_per_chunk

                yield processed_recon

        # Final decoding for remaining tokens
        remaining_tokens = len(token_cache) - n_decoded_tokens
        if remaining_tokens > 0:
            logger.debug(f"Processing {remaining_tokens} remaining tokens")

            tokens_start = max(
                len(token_cache)
                - (self.lookback + self.overlap_frames + remaining_tokens),
                0
            )
            sample_start = (
                len(token_cache)
                - tokens_start
                - remaining_tokens
                - self.overlap_frames
            ) * self.hop_length

            curr_codes = token_cache[tokens_start:]
            recon = self.decoder.decode("".join(curr_codes))
            recon = self.watermarker.apply_watermark(recon, sample_rate=self.sample_rate)
            recon = recon[sample_start:]
            audio_cache.append(recon)

            processed_recon = linear_overlap_add(audio_cache, stride=self.stride_samples)
            processed_recon = processed_recon[n_decoded_samples:]
            yield processed_recon

        logger.info("Streaming TTS processing complete")
