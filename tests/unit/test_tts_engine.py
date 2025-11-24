import pytest
from unittest.mock import MagicMock, patch
from src.tts.engine import NeuTTSAir

@patch('src.tts.engine.Phonemizer')
def test_get_phonemizer(mock_phonemizer_cls):
    # Initialize engine with mocked init to avoid loading models
    with patch.object(NeuTTSAir, '__init__', return_value=None):
        engine = NeuTTSAir()
        engine.phonemizers = {} # Initialize the dict as __init__ would
        
        # First call should create a phonemizer
        engine.get_phonemizer("es")
        mock_phonemizer_cls.assert_called_with(language="es")
        
        # Second call should return cached instance
        mock_phonemizer_cls.reset_mock()
        engine.get_phonemizer("es")
        mock_phonemizer_cls.assert_not_called()
        
        # Call with different language should create new instance
        engine.get_phonemizer("fr-fr")
        mock_phonemizer_cls.assert_called_with(language="fr-fr")