"""
Speech Token Decoder
Decodes neural codec tokens back to audio
"""
import re
import torch
import numpy as np
from src.config.logging_config import get_logger

logger = get_logger(__name__)


class SpeechDecoder:
    """Decodes speech tokens to audio waveform"""

    def __init__(self, codec, is_onnx: bool = False):
        """
        Initialize decoder

        Args:
            codec: Neural codec model for decoding
            is_onnx: Whether using ONNX codec backend
        """
        self.codec = codec
        self.is_onnx = is_onnx

    def decode(self, token_string: str) -> np.ndarray:
        """
        Decode speech tokens to audio

        Args:
            token_string: String containing speech tokens (e.g., "<|speech_0|><|speech_1|>...")

        Returns:
            Audio waveform as numpy array

        Raises:
            ValueError: If no valid speech tokens found
        """
        # Extract speech token IDs using regex
        speech_ids = [int(num) for num in re.findall(r"<\|speech_(\d+)\|>", token_string)]

        if len(speech_ids) == 0:
            raise ValueError("No valid speech tokens found in the output.")

        logger.debug(f"Decoding {len(speech_ids)} speech tokens")

        # ONNX decode
        if self.is_onnx:
            codes = np.array(speech_ids, dtype=np.int32)[np.newaxis, np.newaxis, :]
            recon = self.codec.decode_code(codes)

        # Torch decode
        else:
            with torch.no_grad():
                codes = torch.tensor(speech_ids, dtype=torch.long)[None, None, :].to(
                    self.codec.device
                )
                recon = self.codec.decode_code(codes).cpu().numpy()

        audio = recon[0, 0, :]
        logger.debug(f"Decoded to {len(audio)} audio samples")
        return audio

    def decode_tokens(self, token_ids: list[int]) -> np.ndarray:
        """
        Decode token IDs directly to audio

        Args:
            token_ids: List of token IDs

        Returns:
            Audio waveform as numpy array
        """
        if not token_ids:
            raise ValueError("No token IDs provided")

        logger.debug(f"Decoding {len(token_ids)} token IDs")

        # ONNX decode
        if self.is_onnx:
            codes = np.array(token_ids, dtype=np.int32)[np.newaxis, np.newaxis, :]
            recon = self.codec.decode_code(codes)

        # Torch decode
        else:
            with torch.no_grad():
                codes = torch.tensor(token_ids, dtype=torch.long)[None, None, :].to(
                    self.codec.device
                )
                recon = self.codec.decode_code(codes).cpu().numpy()

        return recon[0, 0, :]
