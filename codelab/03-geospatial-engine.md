# Module 3: The Geospatial Engine (Physical Grounding)

To create a believable 3D world, we need to base our AI textures on real-world geography. In this module, we will implement **Service 2: The Geospatial Engine** to fetch high-resolution satellite imagery from **Google Earth Engine**.

## Grounding the AI
By fetching a real satellite image first, we **ground** the AI, forcing it to repaint over the real physical footprint of the city, preventing spatial hallucinations.

![Architecture: Geospatial Pipeline](./assets/03_geospatial_engine.png)

*This flow diagram shows how the Geospatial Engine translates a pilot's exact latitude and longitude into a raw satellite image tile from the Sentinel-2 dataset.*

---

## Implementation: The `EarthEngineClient`

**Action Marker 3.1:** Terminate the Flask server (CTRL+C). Open `services/geospatial.py`, locate the `[CODELAB STEP 2B]` marker, and paste the following `fetch_satellite_tile` method.

```python
import ee
import requests
from typing import Tuple, List
from config import GCPConfig

class EarthEngineClient:

    @staticmethod
    def fetch_satellite_tile(lat: float, lon: float, offset: float = 0.0025) -> Tuple[bytes, List[float]]:
        # 1. Calculate the geometric spatial bounding box parameters
        area = ee.Geometry.Rectangle([lon - offset, lat - offset, lon + offset, lat + offset])
        
        # 2. Query Copernicus Sentinel-2 data and enforce strict meteorological filters
        collection = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                     .filterBounds(area)
                     .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
                     .sort('system:time_start', False))

        # 3. Extract RGB optical bands and formulate the standardized retrieval URL
        image = collection.first().select(['B4', 'B3', 'B2'])
        thumb_url = image.getThumbURL({
            'region': area, 
            'dimensions': 512, 
            'format': 'png', 
            'min': 0, 
            'max': 3000
        })
        
        # 4. Execute the HTTP GET request to extract the binary image payload
        response = requests.get(thumb_url)
        bounds = [lat - offset, lon - offset, lat + offset, lon + offset]
        
        # Return the raw byte stream and mathematical boundaries
        return response.content, bounds
```

**Action Marker 3.2:** Restart the Flask server (`uv run app.py`).

---

## 🛠 Troubleshooting Earth Engine

If your server crashes when attempting to fetch the tile, check the following:

*   **`403 Forbidden` / User Not Registered:** If you are using a new Google account, you must explicitly accept the terms of service. Visit **[earthengine.google.com/signup](https://earthengine.google.com/signup)** and click "Register", then restart your server.
*   **API Not Enabled:** Ensure the Earth Engine API is enabled in your GCP Console. 
