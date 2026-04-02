import requests
import base64
import json
import os

out_dir = os.path.join("codelab", "assets")
code = """graph LR
Coord[Pilot Lat/Lon] --> Geo[ReverseGeocode Utility]
Geo -->|Google Maps API| API[Geocoding API]
API -->|JSON Data| Geo
Geo -->|City, Country Name| Output"""

state = {
    "code": code,
    "mermaid": {
        "theme": "dark"
    }
}
json_str = json.dumps(state)
b64_str = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
url = f"https://mermaid.ink/img/{b64_str}?type=png"

print("Fetching 03_telemetry_geocoding.png...")
response = requests.get(url)
if response.status_code == 200:
    with open(os.path.join(out_dir, "03_telemetry_geocoding.png"), 'wb') as f:
        f.write(response.content)
    print("Saved 03_telemetry_geocoding.png")
else:
    print("Failed: " + str(response.status_code))
