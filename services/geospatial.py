import requests
from config import GCPConfig, logger
from services.vault import VaultService

class ReverseGeocode:
    """
    Reverse Geocoding Utility using Google Maps API.
    Converts lat/lon to human-readable city names.
    """

    @staticmethod
    def get_location_name(lat: float, lon: float) -> str:
        """
        Calls Google Maps Reverse Geocoding API.
        Returns "City, Country" or "Unknown Location".
        """
        # TODO: [TICKET 1] Implement Reverse Geocoding via Google Maps API
        return "Unknown Location"
