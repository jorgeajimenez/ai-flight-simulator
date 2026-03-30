import ee
import requests
import google.auth
from config import GCPConfig, logger
from typing import Tuple, List

# Initialize Google Earth Engine
try:
    # Explicitly request the Earth Engine scope and force the Project ID
    credentials, _ = google.auth.default(scopes=[
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/earthengine"
    ])
    
    # We force the credentials to use the specific project ID we've configured
    if hasattr(credentials, "with_quota_project"):
        credentials = credentials.with_quota_project(GCPConfig.PROJECT_ID)
        
    ee.Initialize(credentials=credentials, project=GCPConfig.PROJECT_ID)
    logger.info(f"Geospatial: Earth Engine Initialized on {GCPConfig.PROJECT_ID}.")
except Exception as e:
    logger.warning(f"Geospatial: Failed to initialize Earth Engine: {e}")

class EarthEngineClient:
    """
    Geospatial Engine powered by Google Earth Engine.
    Responsible for fetching real-world terrain and satellite textures.
    """
    
    @staticmethod
    def fetch_satellite_tile(lat: float, lon: float, offset: float = 0.0025) -> Tuple[bytes, List[float]]:
        """
        Fetches a high-resolution Sentinel-2 satellite tile for the given coordinates.
        Returns a tuple of (image_bytes, bounds_list).
        """
        try:
            # 1. Calculate bounding box for the tile
            min_lat, max_lat = lat - offset, lat + offset
            min_lon, max_lon = lon - offset, lon + offset
            area = ee.Geometry.Rectangle([min_lon, min_lat, max_lon, max_lat])

            # 2. Filter Sentinel-2 Cloud-Free Collection
            collection = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                         .filterBounds(area)
                         .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
                         .sort('system:time_start', False))
            
            # 3. Process image for RGB display
            image = collection.first().select(['B4', 'B3', 'B2'])
            
            # 4. Generate visual thumbnail URL
            thumb_url = image.getThumbURL({
                'region': area,
                'dimensions': 512,
                'format': 'png',
                'min': 0,
                'max': 3000
            })

            # 5. Download image content
            logger.info(f"Geospatial: Fetching satellite tile at {lat}, {lon}")
            response = requests.get(thumb_url)
            response.raise_for_status()
            
            return response.content, [min_lat, min_lon, max_lat, max_lon]
            
        except Exception as e:
            logger.error(f"Geospatial Error: {e}")
            raise e
