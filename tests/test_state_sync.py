import pytest
from unittest.mock import MagicMock, patch
from services.state_sync import GlobalMultiverseClient

def test_log_terraform_event_success(mocker):
    # 1. Mock the Firestore Client and its methods
    mock_db_instance = MagicMock()
    mocker.patch("services.state_sync.firestore.Client", return_value=mock_db_instance)
    
    mock_collection = MagicMock()
    mock_db_instance.collection.return_value = mock_collection
    
    # Mock firestore.SERVER_TIMESTAMP
    mocker.patch("services.state_sync.firestore.SERVER_TIMESTAMP", "fake-server-timestamp")
    
    # 2. Execute Service
    # Reset singleton if exists
    GlobalMultiverseClient._db = None
    GlobalMultiverseClient.log_terraform_event(37.7749, -122.4194, "Neon Tokyo")
    
    # 3. Assertions
    mock_db_instance.collection.assert_called_with("terraforms")
    mock_collection.add.assert_called_once_with({
        "lat": 37.7749,
        "lon": -122.4194,
        "prompt": "Neon Tokyo",
        "timestamp": "fake-server-timestamp"
    })

def test_log_terraform_event_failure(mocker):
    # Mock client to raise exception
    mocker.patch("services.state_sync.firestore.Client", side_effect=Exception("Firestore API Error"))
    
    # Should not raise exception (graceful failure)
    GlobalMultiverseClient._db = None
    GlobalMultiverseClient.log_terraform_event(0, 0, "Test Fail")
