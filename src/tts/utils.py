"""
TTS Utility Functions
Helper functions for TTS processing
"""
import numpy as np


def linear_overlap_add(frames: list[np.ndarray], stride: int) -> np.ndarray:
    """
    Perform linear overlap-add on audio frames
    Original implementation from: https://github.com/facebookresearch/encodec/blob/main/encodec/utils.py

    Args:
        frames: List of audio frames to combine
        stride: Stride between frames in samples

    Returns:
        Combined audio as numpy array
    """
    assert len(frames)
    dtype = frames[0].dtype
    shape = frames[0].shape[:-1]

    total_size = 0
    for i, frame in enumerate(frames):
        frame_end = stride * i + frame.shape[-1]
        total_size = max(total_size, frame_end)

    sum_weight = np.zeros(total_size, dtype=dtype)
    out = np.zeros(*shape, total_size, dtype=dtype)

    offset: int = 0
    for frame in frames:
        frame_length = frame.shape[-1]
        t = np.linspace(0, 1, frame_length + 2, dtype=dtype)[1:-1]
        weight = np.abs(0.5 - (t - 0.5))

        out[..., offset : offset + frame_length] += weight * frame
        sum_weight[offset : offset + frame_length] += weight
        offset += stride

    assert sum_weight.min() > 0
    return out / sum_weight
