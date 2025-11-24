"""
TTS Service
Business logic for text-to-speech synthesis
"""
import time
from pathlib import Path
from threading import Thread
from typing import Optional
import numpy as np
import soundfile as sf

from src.tts.engine import NeuTTSAir
from src.models.synthesis_request import SynthesisRequest
from src.models.synthesis_response import SynthesisResult
from src.services.session_manager import SessionManager
from src.utils.text_processor import split_text_into_chunks
from src.utils.helpers import generate_timestamp_filename
from src.config.logging_config import get_logger

logger = get_logger(__name__)


class TTSService:
    """Service for managing text-to-speech synthesis"""

    def __init__(
        self,
        session_manager: SessionManager,
        output_folder: Path,
        backbone_repo: str = "neuphonic/neutts-air",
        backbone_device: str = "cpu",
        codec_repo: str = "neuphonic/neucodec",
        codec_device: str = "cpu"
    ):
        """
        Initialize TTS service

        Args:
            session_manager: Session manager for progress tracking
            output_folder: Directory for output files
            backbone_repo: TTS backbone model repository
            backbone_device: Device for backbone model
            codec_repo: Codec model repository
            codec_device: Device for codec model
        """
        self.session_manager = session_manager
        self.output_folder = output_folder
        self._tts_engine: Optional[NeuTTSAir] = None
        self._backbone_repo = backbone_repo
        self._backbone_device = backbone_device
        self._codec_repo = codec_repo
        self._codec_device = codec_device

        # Ensure output folder exists
        self.output_folder.mkdir(parents=True, exist_ok=True)

    def get_tts_engine(self) -> NeuTTSAir:
        """Get or create TTS engine instance (lazy loading)"""
        if self._tts_engine is None:
            logger.info("Initializing TTS engine (first use)")
            self._tts_engine = NeuTTSAir(
                backbone_repo=self._backbone_repo,
                backbone_device=self._backbone_device,
                codec_repo=self._codec_repo,
                codec_device=self._codec_device
            )
        return self._tts_engine

    def synthesize(self, request: SynthesisRequest) -> SynthesisResult:
        """
        Synthesize speech from text

        Args:
            request: Synthesis request with all parameters

        Returns:
            Synthesis result with output file or error
        """
        start_time = time.time()
        session_id = request.session_id

        try:
            # Validate request
            is_valid, error_msg = request.validate()
            if not is_valid:
                logger.error(f"Invalid request: {error_msg}")
                return SynthesisResult.error_result(session_id, error_msg)

            # Step 1: Initialize TTS
            self.session_manager.send_progress(session_id, 1, 'Initializing TTS engine...', 10)
            tts = self.get_tts_engine()

            # Step 2: Encode reference
            self.session_manager.send_progress(session_id, 2, 'Encoding reference audio...', 20)
            ref_codes = tts.encode_reference(request.ref_audio_path)
            logger.info(f"Reference encoded: {ref_codes.shape}")

            # Step 3: Split text into chunks
            self.session_manager.send_progress(session_id, 3, 'Processing text...', 30)
            chunks = split_text_into_chunks(request.input_text, max_tokens=request.max_tokens)
            total_chunks = len(chunks)

            if total_chunks > 1:
                self.session_manager.send_progress(
                    session_id, 3,
                    f'Text split into {total_chunks} chunks for processing...',
                    35
                )

            # Step 4: Generate speech for each chunk
            all_wavs = []
            for i, chunk in enumerate(chunks):
                progress = 40 + (i / total_chunks) * 40  # Progress from 40% to 80%
                self.session_manager.send_progress(
                    session_id, 4,
                    f'Generating speech (chunk {i+1}/{total_chunks})...',
                    int(progress)
                )
                wav = tts.infer(chunk, ref_codes, request.ref_text, language=request.language)
                all_wavs.append(wav)

            # Step 5: Combine audio chunks
            self.session_manager.send_progress(session_id, 5, 'Combining audio chunks...', 85)
            if len(all_wavs) > 1:
                final_wav = np.concatenate(all_wavs)
            else:
                final_wav = all_wavs[0]

            # Step 6: Save output
            self.session_manager.send_progress(session_id, 6, 'Saving audio file...', 95)
            output_filename = generate_timestamp_filename(prefix="output", extension="wav")
            output_path = self.output_folder / output_filename
            sf.write(str(output_path), final_wav, 24000)

            # Calculate duration
            duration_seconds = time.time() - start_time

            # Complete
            self.session_manager.send_progress(session_id, 7, 'Complete!', 100)
            self.session_manager.send_completion(session_id, output_filename, total_chunks)

            logger.info(f"Synthesis complete: {output_filename} ({duration_seconds:.2f}s)")

            return SynthesisResult.success_result(
                session_id=session_id,
                output_file=output_filename,
                output_path=output_path,
                chunks_processed=total_chunks,
                duration_seconds=duration_seconds
            )

        except Exception as e:
            import traceback
            error_msg = f"{str(e)}\n{traceback.format_exc()}"
            logger.error(f"Synthesis error: {error_msg}")
            self.session_manager.send_error(session_id, str(e))

            return SynthesisResult.error_result(session_id, str(e))

    def synthesize_async(self, request: SynthesisRequest):
        """
        Start asynchronous synthesis in background thread

        Args:
            request: Synthesis request
        """
        thread = Thread(target=self.synthesize, args=(request,))
        thread.daemon = True
        thread.start()
        logger.info(f"Started async synthesis for session: {request.session_id}")


# Global TTS service instance
_tts_service: Optional[TTSService] = None


def get_tts_service(
    session_manager: SessionManager,
    output_folder: Path,
    **kwargs
) -> TTSService:
    """
    Get or create global TTS service instance

    Args:
        session_manager: Session manager
        output_folder: Output directory
        **kwargs: Additional TTS configuration

    Returns:
        TTSService instance
    """
    global _tts_service
    if _tts_service is None:
        _tts_service = TTSService(session_manager, output_folder, **kwargs)
    return _tts_service
