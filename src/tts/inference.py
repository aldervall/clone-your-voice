"""
TTS Inference Engine
Handles inference with torch and GGML backends
"""
import torch
from typing import Generator
from src.config.logging_config import get_logger

logger = get_logger(__name__)


class TorchInference:
    """Inference using PyTorch backend"""

    def __init__(self, backbone, tokenizer, max_context: int = 2048):
        """
        Initialize torch inference

        Args:
            backbone: Transformer model
            tokenizer: HuggingFace tokenizer
            max_context: Maximum context length
        """
        self.backbone = backbone
        self.tokenizer = tokenizer
        self.max_context = max_context

    def apply_chat_template(
        self,
        ref_codes: list[int],
        ref_text: str,
        input_text: str
    ) -> list[int]:
        """
        Apply chat template to create model input

        Args:
            ref_codes: Reference audio codes
            ref_text: Phonemized reference text
            input_text: Phonemized input text

        Returns:
            Token IDs for model input
        """
        # Combine texts
        full_text = ref_text + " " + input_text

        # Get special tokens
        speech_replace = self.tokenizer.convert_tokens_to_ids("<|SPEECH_REPLACE|>")
        speech_gen_start = self.tokenizer.convert_tokens_to_ids("<|SPEECH_GENERATION_START|>")
        text_replace = self.tokenizer.convert_tokens_to_ids("<|TEXT_REPLACE|>")
        text_prompt_start = self.tokenizer.convert_tokens_to_ids("<|TEXT_PROMPT_START|>")
        text_prompt_end = self.tokenizer.convert_tokens_to_ids("<|TEXT_PROMPT_END|>")

        # Encode text
        input_ids = self.tokenizer.encode(full_text, add_special_tokens=False)

        # Create chat template
        chat = """user: Convert the text to speech:<|TEXT_REPLACE|>\nassistant:<|SPEECH_REPLACE|>"""
        ids = self.tokenizer.encode(chat)

        # Replace text placeholder
        text_replace_idx = ids.index(text_replace)
        ids = (
            ids[:text_replace_idx]
            + [text_prompt_start]
            + input_ids
            + [text_prompt_end]
            + ids[text_replace_idx + 1 :]
        )

        # Replace speech placeholder with reference codes
        speech_replace_idx = ids.index(speech_replace)
        codes_str = "".join([f"<|speech_{i}|>" for i in ref_codes])
        codes = self.tokenizer.encode(codes_str, add_special_tokens=False)
        ids = ids[:speech_replace_idx] + [speech_gen_start] + list(codes)

        return ids

    def infer(self, prompt_ids: list[int]) -> str:
        """
        Run inference to generate speech tokens

        Args:
            prompt_ids: Input token IDs

        Returns:
            Generated token string
        """
        prompt_tensor = torch.tensor(prompt_ids).unsqueeze(0).to(self.backbone.device)
        speech_end_id = self.tokenizer.convert_tokens_to_ids("<|SPEECH_GENERATION_END|>")

        logger.debug(f"Running torch inference with prompt length: {len(prompt_ids)}")

        with torch.no_grad():
            output_tokens = self.backbone.generate(
                prompt_tensor,
                max_length=self.max_context,
                eos_token_id=speech_end_id,
                do_sample=True,
                temperature=1.0,
                top_k=50,
                use_cache=True,
                min_new_tokens=50,
            )

        input_length = prompt_tensor.shape[-1]
        output_str = self.tokenizer.decode(
            output_tokens[0, input_length:].cpu().numpy().tolist(),
            add_special_tokens=False
        )

        logger.debug(f"Generated {len(output_str)} characters of tokens")
        return output_str


class GGMLInference:
    """Inference using GGML/llama.cpp backend"""

    def __init__(self, backbone, max_context: int = 2048):
        """
        Initialize GGML inference

        Args:
            backbone: Llama.cpp model
            max_context: Maximum context length
        """
        self.backbone = backbone
        self.max_context = max_context

    def create_prompt(
        self,
        ref_codes: list[int],
        ref_text: str,
        input_text: str
    ) -> str:
        """
        Create prompt for GGML inference

        Args:
            ref_codes: Reference audio codes
            ref_text: Phonemized reference text
            input_text: Phonemized input text

        Returns:
            Formatted prompt string
        """
        codes_str = "".join([f"<|speech_{idx}|>" for idx in ref_codes])
        prompt = (
            f"user: Convert the text to speech:<|TEXT_PROMPT_START|>{ref_text} {input_text}"
            f"<|TEXT_PROMPT_END|>\nassistant:<|SPEECH_GENERATION_START|>{codes_str}"
        )
        return prompt

    def infer(self, ref_codes: list[int], ref_text: str, input_text: str) -> str:
        """
        Run GGML inference

        Args:
            ref_codes: Reference audio codes
            ref_text: Phonemized reference text
            input_text: Phonemized input text

        Returns:
            Generated token string
        """
        prompt = self.create_prompt(ref_codes, ref_text, input_text)
        logger.debug(f"Running GGML inference with prompt length: {len(prompt)}")

        output = self.backbone(
            prompt,
            max_tokens=self.max_context,
            temperature=1.0,
            top_k=50,
            stop=["<|SPEECH_GENERATION_END|>"],
        )

        output_str = output["choices"][0]["text"]
        logger.debug(f"Generated {len(output_str)} characters of tokens")
        return output_str

    def infer_stream(
        self,
        ref_codes: list[int],
        ref_text: str,
        input_text: str
    ) -> Generator[str, None, None]:
        """
        Run streaming GGML inference

        Args:
            ref_codes: Reference audio codes
            ref_text: Phonemized reference text
            input_text: Phonemized input text

        Yields:
            Generated token strings
        """
        prompt = self.create_prompt(ref_codes, ref_text, input_text)
        logger.debug(f"Running streaming GGML inference")

        for item in self.backbone(
            prompt,
            max_tokens=self.max_context,
            temperature=1.0,
            top_k=50,
            stop=["<|SPEECH_GENERATION_END|>"],
            stream=True
        ):
            output_str = item["choices"][0]["text"]
            yield output_str
