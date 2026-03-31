import pytest
import base64
from unittest.mock import MagicMock, patch
from services.audio_engine import AudioSynthesisService


def test_synthesize_advisory_success(mocker):
    # 1. Mock the TextToSpeechClient
    mock_client_class = mocker.patch(
        "services.audio_engine.texttospeech.TextToSpeechClient"
    )
    mock_client_instance = MagicMock()
    mock_client_class.return_value = mock_client_instance

    # 2. Mock the response
    mock_response = MagicMock()
    mock_response.audio_content = b"fake-mp3-audio-bytes"
    mock_client_instance.synthesize_speech.return_value = mock_response

    # 3. Execute Service
    audio_b64 = AudioSynthesisService.synthesize_advisory("Welcome pilot.")

    # 4. Assertions
    expected_b64 = base64.b64encode(b"fake-mp3-audio-bytes").decode("utf-8")
    assert audio_b64 == expected_b64

    # Verify the correct voice was requested
    mock_client_instance.synthesize_speech.assert_called_once()
    args, kwargs = mock_client_instance.synthesize_speech.call_args
    voice_params = kwargs["voice"]
    assert voice_params.name == "en-US-Studio-O"


def test_synthesize_advisory_failure(mocker):
    # Mock client to raise exception
    mock_client_class = mocker.patch(
        "services.audio_engine.texttospeech.TextToSpeechClient"
    )
    mock_client_instance = MagicMock()
    mock_client_class.return_value = mock_client_instance
    mock_client_instance.synthesize_speech.side_effect = Exception("TTS API Error")

    # Should return empty string on failure
    audio_b64 = AudioSynthesisService.synthesize_advisory("Error test.")
    assert audio_b64 == ""
