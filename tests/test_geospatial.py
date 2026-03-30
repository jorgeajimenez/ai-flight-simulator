import pytest
from unittest.mock import MagicMock, patch
from services.geospatial import EarthEngineClient

def test_fetch_satellite_tile_success(mocker):
    # Mock ee.Initialize
    mocker.patch("ee.Initialize")
    # Mock ee.Geometry.Rectangle
    mock_region = MagicMock()
    mocker.patch("ee.Geometry.Rectangle", return_value=mock_region)
    # Mock ee.ImageCollection
    mock_s2 = MagicMock()
    mocker.patch("ee.ImageCollection", return_value=mock_s2)
    # Mock chain of calls for ee.ImageCollection
    mock_image = MagicMock()
    mock_s2.filterBounds.return_value.filterDate.return_value.sort.return_value.first.return_value.clip.return_value = mock_image
    
    # Mock image.getThumbURL
    mock_image.getThumbURL.return_value = "http://fake-url.com/image.png"
    
    # Mock requests.get
    mock_response = MagicMock()
    mock_response.content = b"fake-image-bytes"
    mock_response.status_code = 200
    mocker.patch("requests.get", return_value=mock_response)

    # Set initialized flag to skip actual init logic in test
    EarthEngineClient._initialized = True
    
    content, bounds = EarthEngineClient.fetch_satellite_tile(37.0, -122.0)
    
    assert content == b"fake-image-bytes"
    assert len(bounds) == 4
    # Check that bounds were calculated with offset 0.0025
    assert bounds == [37.0 - 0.0025, -122.0 - 0.0025, 37.0 + 0.0025, -122.0 + 0.0025]

def test_init_ee_local_key(mocker):
    # Reset initialization
    EarthEngineClient._initialized = False
    
    # Mock ee.Initialize
    mock_init = mocker.patch("ee.Initialize")
    # Mock ee.data (to avoid attribute errors if checked)
    mocker.patch("ee.data", spec=[]) 
    
    # Mock os.path.exists for the local key file
    mocker.patch("os.path.exists", return_value=True)
    
    # Mock service_account.Credentials
    mock_creds = MagicMock()
    mocker.patch("google.oauth2.service_account.Credentials.from_service_account_file", return_value=mock_creds)
    mock_scoped_creds = MagicMock()
    mock_creds.with_scopes.return_value = mock_scoped_creds
    
    EarthEngineClient._init_ee()
    
    assert EarthEngineClient._initialized == True
    mock_init.assert_called_once()
