import pytest
import base64
from unittest.mock import MagicMock
from services.audio_engine import AudioSynthesisService

def test_synthesize_advisory_success(mocker):
    mock_client_class = mocker.patch("services.audio_engine.texttospeech.TextToSpeechClient")
    mock_client_instance = MagicMock()
    mock_client_class.return_value = mock_client_instance
    mock_response = MagicMock()
    mock_response.audio_content = b"fake-audio-bytes"
    mock_client_instance.synthesize_speech.return_value = mock_response

    audio_b64 = AudioSynthesisService.synthesize_advisory("Test.", voice_type="pilot")
    assert audio_b64 == base64.b64encode(b"fake-audio-bytes").decode("utf-8")

def test_synthesize_advisory_failure(mocker):
    mock_client_class = mocker.patch("services.audio_engine.texttospeech.TextToSpeechClient")
    mock_client_instance = MagicMock()
    mock_client_class.return_value = mock_client_instance
    mock_client_instance.synthesize_speech.side_effect = Exception("TTS API Error")

    with pytest.raises(Exception):
        AudioSynthesisService.synthesize_advisory("Error test.")