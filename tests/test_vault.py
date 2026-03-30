import pytest
from unittest.mock import MagicMock
from services.vault import VaultService

def test_get_maps_api_key_cached(mocker):
    VaultService._api_key_cache = "cached-key"
    key = VaultService.get_maps_api_key()
    assert key == "cached-key"
    VaultService._api_key_cache = None

def test_get_maps_api_key_from_secret_manager(mocker):
    VaultService._api_key_cache = None
    
    # Mock Secret Manager client
    mock_client = MagicMock()
    mocker.patch("google.cloud.secretmanager.SecretManagerServiceClient", return_value=mock_client)
    
    mock_response = MagicMock()
    mock_response.payload.data = b"secret-manager-key"
    mock_client.access_secret_version.return_value = mock_response
    
    key = VaultService.get_maps_api_key()
    
    assert key == "secret-manager-key"
    mock_client.access_secret_version.assert_called_once()
    assert VaultService._api_key_cache == "secret-manager-key"

def test_get_maps_api_key_fallback(mocker):
    VaultService._api_key_cache = None
    
    # Mock Secret Manager to raise an error
    mocker.patch("google.cloud.secretmanager.SecretManagerServiceClient", side_effect=Exception("API Error"))
    
    # Mock OS environ fallback
    mocker.patch("os.environ.get", return_value="env-fallback-key")
    
    key = VaultService.get_maps_api_key()
    
    assert key == "env-fallback-key"
