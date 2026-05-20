# Ticket #1: Reverse Geocoding Utility

**Status:** TODO
**Module:** `services/geospatial.py`

## Background
The AI currently lacks spatial awareness. When the pilot flies over a location, the telemetry provides raw latitude and longitude, but the AI needs a human-readable city and country name to ground its generative responses.

## Engineering Specification
Implement the `get_location_name(lat: float, lon: float) -> str` method within the `ReverseGeocode` class.

### Requirements:
1. **API Integration:** Call the Google Maps Geocoding API (`https://maps.googleapis.com/maps/api/geocode/json`).
2. **Authentication:** Securely fetch the API key using `VaultService.get_maps_api_key()`.
3. **Data Extraction:** Parse the JSON response. Look within `address_components` to extract the `locality` (City) and `country`.
4. **Return Format:** 
   - If both are found: Return `"{City}, {Country}"`.
   - If only country is found: Return `"{Country}"`.
   - On network failure, zero results, or missing API key: Return `"Unknown Location"`.

### Constraints
- Do **not** hardcode any API keys.
- Handle all HTTP exceptions gracefully to prevent server crashes.