import pytest
from unittest.mock import MagicMock, patch
from services.geospatial import ReverseGeocode

def test_reverse_geocode_success(mocker):
    # Mock the vault to return a dummy API key
    mocker.patch("services.vault.VaultService.get_maps_api_key", return_value="dummy_key")
    
    # Mock the requests.get to return a mock Google Maps API response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "status": "OK",
        "results": [
            {
                "address_components": [
                    {"long_name": "Paris", "types": ["locality"]},
                    {"long_name": "France", "types": ["country"]}
                ]
            }
        ]
    }
    mocker.patch("requests.get", return_value=mock_response)
    
    city = ReverseGeocode.get_location_name(48.8566, 2.3522)
    assert city == "Paris, France"

def test_reverse_geocode_no_key(mocker):
    # Mock the vault to return None (no key found)
    mocker.patch("services.vault.VaultService.get_maps_api_key", return_value=None)
    
    city = ReverseGeocode.get_location_name(48.8566, 2.3522)
    assert city == "Unknown Location"
