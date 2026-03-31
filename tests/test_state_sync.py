import pytest
from unittest.mock import MagicMock, patch
from services.state_sync import PersistentWorldClient


def test_log_terraform_event_success(mocker):
    # 1. Mock the Firestore Client and Storage Client
    mock_db_instance = MagicMock()
    mocker.patch("services.state_sync.firestore.Client", return_value=mock_db_instance)

    mock_storage_instance = MagicMock()
    mocker.patch(
        "services.state_sync.storage.Client", return_value=mock_storage_instance
    )

    mock_bucket = MagicMock()
    mock_storage_instance.get_bucket.return_value = mock_bucket
    mock_blob = MagicMock()
    mock_bucket.blob.return_value = mock_blob
    mock_blob.public_url = "http://fake-texture-url.png"

    mock_collection = MagicMock()
    mock_db_instance.collection.return_value = mock_collection

    # Mock firestore.SERVER_TIMESTAMP
    mocker.patch(
        "services.state_sync.firestore.SERVER_TIMESTAMP", "fake-server-timestamp"
    )

    # 2. Execute Service
    fake_b64 = "ZmFrZS1pbWFnZS1kYXRh"  # "fake-image-data" in base64
    url = PersistentWorldClient.log_terraform_event(
        37.7749, -122.4194, "Neon Tokyo", fake_b64
    )

    # 3. Assertions
    assert url == "http://fake-texture-url.png"
    mock_db_instance.collection.assert_called_with("terraforms")
    mock_collection.add.assert_called_once()
    args, kwargs = mock_collection.add.call_args
    assert args[0]["latitude"] == 37.7749
    assert args[0]["prompt"] == "Neon Tokyo"


def test_log_terraform_event_failure(mocker):
    # Mock client to raise exception
    mocker.patch(
        "services.state_sync.storage.Client", side_effect=Exception("Storage Error")
    )

    # Should not raise exception (graceful failure)
    url = PersistentWorldClient.log_terraform_event(0, 0, "Test Fail", "b64")
    assert url == ""
