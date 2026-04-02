import pytest
import base64
import json
from unittest.mock import MagicMock
from services.ai_vision import AIVisionService

def test_generate_biome_texture_success(mocker):
    # 1. Mock the GenAI client
    mock_genai = mocker.patch("services.ai_vision.genai.Client")
    mock_client_instance = MagicMock()
    mock_genai.return_value = mock_client_instance

    # Mock Gemini response (The mandated JSON structure)
    mock_gemini_res = MagicMock()
    mock_gemini_res.text = json.dumps(
        {
            "advisory": "Pilot, prepare for neon entry.",
            "imagen_prompt": "A photorealistic high-resolution aerial view of a cyberpunk city.",
        }
    )
    mock_client_instance.models.generate_content.return_value = mock_gemini_res

    # Mock Imagen 3 response
    mock_imagen_res = MagicMock()
    mock_generated_image = MagicMock()
    mock_generated_image.image_bytes = b"generated-texture-bytes"
    mock_imagen_res.generated_images = [mock_generated_image]
    mock_client_instance.models.generate_images.return_value = mock_imagen_res

    # 3. Execute Service
    result = AIVisionService.generate_biome_texture(
        "Paris", "Cyberpunk City"
    )

    # 4. Assertions
    assert result["advisory"] == "Pilot, prepare for neon entry."
    
    # Verify image was base64 encoded
    expected_b64 = base64.b64encode(b"generated-texture-bytes").decode("utf-8")
    assert result["image_b64"] == expected_b64
