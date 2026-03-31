import pytest
import base64
import json
from unittest.mock import MagicMock, patch
from services.ai_vision import AIVisionService


def test_analyze_and_terraform_success(mocker):
    # 1. Mock the classes in the service namespace
    mock_gemini_class = mocker.patch("services.ai_vision.GenerativeModel")
    mock_gemini_instance = MagicMock()
    mock_gemini_class.return_value = mock_gemini_instance

    mocker.patch("services.ai_vision.Part.from_data")

    # Mock Gemini response (The mandated JSON structure)
    mock_gemini_res = MagicMock()
    mock_gemini_res.text = json.dumps(
        {
            "advisory": "Pilot, prepare for neon entry.",
            "imagen_prompt": "A photorealistic high-resolution aerial view of a cyberpunk city.",
        }
    )
    mock_gemini_instance.generate_content.return_value = mock_gemini_res

    # 2. Mock ImageGenerationModel (Imagen 3) in the service namespace
    mock_imagen_class = mocker.patch(
        "services.ai_vision.ImageGenerationModel.from_pretrained"
    )
    mock_imagen_model = MagicMock()
    mock_imagen_class.return_value = mock_imagen_model

    mocker.patch("services.ai_vision.VertexImage")

    # Mock the generated image response
    mock_generated_image = MagicMock()
    mock_imagen_model.edit_image.return_value = [mock_generated_image]

    # Mock the save method of the generated image to simulate writing bytes
    def mock_save(buffer, include_generation_parameters=False):
        buffer.write(b"generated-texture-bytes")

    mock_generated_image.save.side_effect = mock_save

    # 3. Execute Service
    result = AIVisionService.analyze_and_terraform(
        b"original-satellite-bytes", "Cyberpunk City"
    )

    # 4. Assertions
    assert result["advisory"] == "Pilot, prepare for neon entry."
    # Verify image was base64 encoded
    expected_b64 = base64.b64encode(b"generated-texture-bytes").decode("utf-8")
    assert result["image_b64"] == expected_b64
