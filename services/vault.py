import logging
from google.cloud import secretmanager
from config import GCPConfig, logger

class VaultService:
    """
    Secure Key Management Service.
    Handles retrieval and local caching of API keys and secrets from GCP Secret Manager.
    """
    _cache: dict[str, str] = {}

    @classmethod
    def get_maps_api_key(cls, secret_id: str = "GOOGLE_MAPS_API_KEY") -> str:
        """
        Fetches the Google Maps API Key from Secret Manager.
        Uses in-memory caching to reduce redundant API calls and latency.
        """
        if secret_id in cls._cache:
            return cls._cache[secret_id]

        try:
            logger.info(f"Vault: Accessing secret {secret_id}...")
            client = secretmanager.SecretManagerServiceClient()
            name = f"projects/{GCPConfig.PROJECT_ID}/secrets/{secret_id}/versions/latest"
            response = client.access_secret_version(request={"name": name})
            
            key = response.payload.data.decode("UTF-8")
            cls._cache[secret_id] = key
            return key
        except Exception as e:
            logger.error(f"Vault Error: Failed to fetch {secret_id}: {e}")
            # AI_WIRING_POINT: Secret Recovery Strategy (Fall back to env or local)
            return ""
