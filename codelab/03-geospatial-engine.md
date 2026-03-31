# Module 3: The Geospatial Engine (Grounded Vision)

To create a believable 3D world, we need to base our AI textures on real-world geography. In this module, we will implement **Service 2: The Geospatial Engine** to fetch high-resolution satellite imagery from **Google Earth Engine**.

## Grounding the AI
A major challenge with Generative AI is "hallucination." If we just ask an AI to "draw Tokyo," it might get the buildings right but the street layout wrong. By fetching a real satellite image first, we **ground** the AI, forcing it to repaint over the real physical footprint of the city.

![Architecture: Geospatial Pipeline](./assets/03_geospatial_engine.png)

## Why Earth Engine?
While standard map APIs provide tiles for navigation, **Google Earth Engine** provides programmatic access to petabytes of scientific satellite data (like Sentinel-2). This allows us to fetch the raw data we need to feed our generative AI "terraforming" pipeline.

## Implementation: The `EarthEngineClient`

We encapsulate the complex Earth Engine SDK logic into a clean `fetch_satellite_tile` method. Before we can query the data, we must initialize the client explicitly using the project quota.

### Initialization (`services/geospatial.py`)
```python
# Explicitly request the Earth Engine scope and force the Project ID
credentials, _ = google.auth.default(scopes=[
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/earthengine"
])

# Force the credentials to use the specific project quota
if hasattr(credentials, "with_quota_project"):
    credentials = credentials.with_quota_project(GCPConfig.PROJECT_ID)
    
ee.Initialize(credentials=credentials, project=GCPConfig.PROJECT_ID)
```

### Fetching the Tile
The `fetch_satellite_tile` method performs three critical steps:
1.  **Calculate bounding box:** Defines the 500m x 500m area based on the pilot's coordinates.
2.  **Dataset Filtering:** Queries the `COPERNICUS/S2_SR_HARMONIZED` collection, filtering for the clearest (least cloudy) images.
3.  **Tile Extraction:** Downloads and returns the raw bytes.

```python
@staticmethod
def fetch_satellite_tile(lat: float, lon: float, offset: float = 0.0025) -> Tuple[bytes, List[float]]:
    # 1. Calculate bounding box
    area = ee.Geometry.Rectangle([lon - offset, lat - offset, lon + offset, lat + offset])
    
    # 2. Filter for the clearest satellite image
    collection = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                 .filterBounds(area)
                 .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
                 .sort('system:time_start', False))

    # 3. Process image and generate a download URL
    image = collection.first().select(['B4', 'B3', 'B2'])
    thumb_url = image.getThumbURL({'region': area, 'dimensions': 512, 'format': 'png', 'min': 0, 'max': 3000})
    
    # 4. Download and return the raw bytes
    response = requests.get(thumb_url)
    return response.content, [lat - offset, lon - offset, lat + offset, lon + offset]
```

## AI Wiring Point

In our main `app.py`, we can now "wire up" the geospatial engine with a single line of code:

```python
# AI_WIRING_POINT: Geospatial Fetch
image_bytes, bounds = EarthEngineClient.fetch_satellite_tile(lat, lon)
```

By isolating this logic, we keep our main application logic focused purely on orchestration.