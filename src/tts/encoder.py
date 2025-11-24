"""
Reference Audio Encoder
Encodes reference audio into neural codec tokens
"""
from pathlib import Path
import librosa
import torch
import numpy as np
from src.config.logging_config import get_logger

logger = get_logger(__name__)


class ReferenceEncoder:
    """Encodes reference audio for voice cloning"""

    def __init__(self, codec, sample_rate: int = 16000):
        """
        Initialize encoder

        Args:
            codec: Neural codec model for encoding
            sample_rate: Sample rate for audio loading
        """
        self.codec = codec
        self.sample_rate = sample_rate

    def encode(self, audio_path: str | Path) -> np.ndarray | torch.Tensor:
        """
        Encode reference audio to codec tokens

        Args:
            audio_path: Path to reference audio file

        Returns:
            Encoded reference codes
        """
        logger.info(f"Encoding reference audio: {audio_path}")

        # Load audio
        wav, _ = librosa.load(audio_path, sr=self.sample_rate, mono=True)
        logger.debug(f"Loaded audio: {len(wav)} samples at {self.sample_rate}Hz")

        # Convert to tensor
        wav_tensor = torch.from_numpy(wav).float().unsqueeze(0).unsqueeze(0)  # [1, 1, T]

        # Encode
        with torch.no_grad():
            ref_codes = self.codec.encode_code(audio_or_path=wav_tensor).squeeze(0).squeeze(0)

        logger.info(f"Reference encoded to {ref_codes.shape} shape, {ref_codes.numel()} tokens")
        return ref_codes
