"""
NeuTTS-Air TTS Engine
Main orchestrator for text-to-speech synthesis
"""
from pathlib import Path
from typing import Generator, Optional
import torch
import numpy as np
import perth
from neucodec import NeuCodec, DistillNeuCodec

from src.tts.phonemizer import Phonemizer
from src.tts.encoder import ReferenceEncoder
from src.tts.decoder import SpeechDecoder
from src.tts.inference import TorchInference, GGMLInference
from src.tts.streaming import StreamingProcessor
from src.config.logging_config import get_logger

logger = get_logger(__name__)


class NeuTTSAir:
    """
    NeuTTS-Air text-to-speech engine
    Orchestrates phonemization, encoding, inference, and decoding
    """

    def __init__(
        self,
        backbone_repo: str = "neuphonic/neutts-air",
        backbone_device: str = "cpu",
        codec_repo: str = "neuphonic/neucodec",
        codec_device: str = "cpu",
    ):
        """
        Initialize TTS engine

        Args:
            backbone_repo: HuggingFace repo or GGUF file path for backbone model
            backbone_device: Device for backbone (cpu/cuda)
            codec_repo: HuggingFace repo for codec
            codec_device: Device for codec (cpu/cuda)
        """
        # Configuration
        self.sample_rate = 24_000
        self.max_context = 2048
        self.hop_length = 480

        # Streaming configuration
        self.streaming_overlap_frames = 1
        self.streaming_frames_per_chunk = 25
        self.streaming_lookforward = 5
        self.streaming_lookback = 50
        self.streaming_stride_samples = self.streaming_frames_per_chunk * self.hop_length

        # Backend flags
        self._is_quantized_model = False
        self._is_onnx_codec = False

        # Initialize components
        logger.info("Initializing NeuTTS-Air engine")

        # Load phonemizer
        self.phonemizer = Phonemizer()

        # Load backbone model
        self._load_backbone(backbone_repo, backbone_device)

        # Load codec
        self._load_codec(codec_repo, codec_device)

        # Initialize encoder and decoder
        self.encoder = ReferenceEncoder(self.codec, sample_rate=16000)
        self.decoder = SpeechDecoder(self.codec, is_onnx=self._is_onnx_codec)

        # Load watermarker
        logger.info("Loading audio watermarker")
        self.watermarker = perth.PerthImplicitWatermarker()

        # Initialize streaming processor
        self.streaming_processor = StreamingProcessor(
            decoder=self.decoder,
            watermarker=self.watermarker,
            hop_length=self.hop_length,
            frames_per_chunk=self.streaming_frames_per_chunk,
            lookforward=self.streaming_lookforward,
            lookback=self.streaming_lookback,
            overlap_frames=self.streaming_overlap_frames,
            sample_rate=self.sample_rate
        )

        logger.info("NeuTTS-Air engine initialized successfully")

    def _load_backbone(self, backbone_repo: str, backbone_device: str):
        """Load backbone model (transformer or GGUF)"""
        logger.info(f"Loading backbone from: {backbone_repo} on {backbone_device}")

        # GGUF loading
        if backbone_repo.endswith("gguf"):
            try:
                from llama_cpp import Llama
            except ImportError as e:
                raise ImportError(
                    "Failed to import `llama_cpp`. "
                    "Please install it with:\n"
                    "    pip install llama-cpp-python"
                ) from e

            self.backbone = Llama.from_pretrained(
                repo_id=backbone_repo,
                filename="*.gguf",
                verbose=False,
                n_gpu_layers=-1 if backbone_device == "gpu" else 0,
                n_ctx=self.max_context,
                mlock=True,
                flash_attn=True if backbone_device == "gpu" else False,
            )
            self._is_quantized_model = True
            self.inference_engine = GGMLInference(self.backbone, self.max_context)
            self.tokenizer = None

        else:
            from transformers import AutoTokenizer, AutoModelForCausalLM

            self.tokenizer = AutoTokenizer.from_pretrained(backbone_repo)
            self.backbone = AutoModelForCausalLM.from_pretrained(backbone_repo).to(
                torch.device(backbone_device)
            )
            self.inference_engine = TorchInference(
                self.backbone, self.tokenizer, self.max_context
            )

    def _load_codec(self, codec_repo: str, codec_device: str):
        """Load neural codec model"""
        logger.info(f"Loading codec from: {codec_repo} on {codec_device}")

        match codec_repo:
            case "neuphonic/neucodec":
                self.codec = NeuCodec.from_pretrained(codec_repo)
                self.codec.eval().to(codec_device)

            case "neuphonic/distill-neucodec":
                self.codec = DistillNeuCodec.from_pretrained(codec_repo)
                self.codec.eval().to(codec_device)

            case "neuphonic/neucodec-onnx-decoder":
                if codec_device != "cpu":
                    raise ValueError("ONNX decoder only currently runs on CPU.")

                try:
                    from neucodec import NeuCodecOnnxDecoder
                except ImportError as e:
                    raise ImportError(
                        "Failed to import the onnx decoder."
                        " Ensure you have onnxruntime installed as well as neucodec >= 0.0.4."
                    ) from e

                self.codec = NeuCodecOnnxDecoder.from_pretrained(codec_repo)
                self._is_onnx_codec = True

            case _:
                raise ValueError(
                    "Invalid codec repo! Must be one of:"
                    " 'neuphonic/neucodec', 'neuphonic/distill-neucodec',"
                    " 'neuphonic/neucodec-onnx-decoder'."
                )

    def encode_reference(self, ref_audio_path: str | Path) -> np.ndarray | torch.Tensor:
        """
        Encode reference audio

        Args:
            ref_audio_path: Path to reference audio file

        Returns:
            Encoded reference codes
        """
        return self.encoder.encode(ref_audio_path)

    def infer(
        self,
        text: str,
        ref_codes: np.ndarray | torch.Tensor,
        ref_text: str
    ) -> np.ndarray:
        """
        Perform inference to generate speech from text

        Args:
            text: Input text to be converted to speech
            ref_codes: Encoded reference audio
            ref_text: Reference text for reference audio

        Returns:
            Generated speech waveform
        """
        logger.info(f"Running TTS inference for text: '{text[:50]}...'")

        # Phonemize texts
        ref_text_phones = self.phonemizer.phonemize(ref_text)
        input_text_phones = self.phonemizer.phonemize(text)

        # Generate tokens
        if self._is_quantized_model:
            output_str = self.inference_engine.infer(ref_codes, ref_text_phones, input_text_phones)
        else:
            prompt_ids = self.inference_engine.apply_chat_template(
                ref_codes, ref_text_phones, input_text_phones
            )
            output_str = self.inference_engine.infer(prompt_ids)

        # Decode to audio
        wav = self.decoder.decode(output_str)

        # Apply watermark
        watermarked_wav = self.watermarker.apply_watermark(wav, sample_rate=self.sample_rate)

        logger.info(f"Generated {len(watermarked_wav)} audio samples")
        return watermarked_wav

    def infer_stream(
        self,
        text: str,
        ref_codes: np.ndarray | torch.Tensor,
        ref_text: str
    ) -> Generator[np.ndarray, None, None]:
        """
        Perform streaming inference to generate speech

        Args:
            text: Input text to be converted to speech
            ref_codes: Encoded reference audio
            ref_text: Reference text for reference audio

        Yields:
            Audio chunks as numpy arrays
        """
        if not self._is_quantized_model:
            raise NotImplementedError("Streaming is not implemented for the torch backend!")

        logger.info(f"Running streaming TTS inference for text: '{text[:50]}...'")

        # Phonemize texts
        ref_text_phones = self.phonemizer.phonemize(ref_text)
        input_text_phones = self.phonemizer.phonemize(text)

        # Get streaming token generator
        token_generator = self.inference_engine.infer_stream(
            ref_codes, ref_text_phones, input_text_phones
        )

        # Process stream
        yield from self.streaming_processor.process_stream(token_generator, ref_codes)
