import pytest
import json
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_terraform_orchestration_success(client, mocker):
    # 1. Mock all services for V2 pipeline
    mock_geo = mocker.patch("services.geospatial.ReverseGeocode.get_location_name")
    mock_geo.return_value = "Neo Tokyo"

    mock_vision = mocker.patch(
        "services.ai_vision.AIVisionService.generate_biome_texture"
    )
    mock_vision.return_value = {
        "image_b64": "fake-image",
        "advisory": "Neon skies ahead.",
    }

    mock_audio = mocker.patch(
        "services.audio_engine.AudioSynthesisService.synthesize_advisory"
    )
    mock_audio.return_value = "fake-audio-b64"

    mock_sync = mocker.patch(
        "services.state_sync.PersistentWorldClient.log_terraform_event"
    )
    mock_sync.return_value = "http://cdn/texture.png"

    # 2. Execute Request
    payload = {"lat": 37.0, "lon": -122.0, "prompt": "Cyberpunk"}
    response = client.post(
        "/terraform", data=json.dumps(payload), content_type="application/json"
    )

    # 3. Assertions
    assert response.status_code == 200
    data = json.loads(response.data)

    assert data["image"] == "fake-image"
    assert data["audio"] == "fake-audio-b64"
    assert data["narrative"] == "Neon skies ahead."
    assert data["texture_url"] == "http://cdn/texture.png"
    assert data["city"] == "Neo Tokyo"
    assert "bounds" in data

    # Verify orchestration order and arguments
    mock_geo.assert_called_once_with(37.0, -122.0)
    mock_vision.assert_called_once_with("Neo Tokyo", "Cyberpunk")
    mock_audio.assert_called_once_with("Neon skies ahead.")
    mock_sync.assert_called_once_with(37.0, -122.0, "Cyberpunk", "fake-image")


def test_terraform_orchestration_failure(client, mocker):
    # Mock one service to fail
    mocker.patch(
        "services.geospatial.ReverseGeocode.get_location_name",
        side_effect=Exception("Geospatial Error"),
    )

    response = client.post(
        "/terraform",
        data=json.dumps({"lat": 0, "lon": 0}),
        content_type="application/json",
    )

    assert response.status_code == 500
    data = json.loads(response.data)
    assert "error" in data
    assert "Geospatial Error" in data["error"]
