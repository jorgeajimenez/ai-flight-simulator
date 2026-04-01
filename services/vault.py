import os
from google.cloud import secretmanager
from config import GCPConfig

class VaultService:
    # Initialize an in-memory dictionary to cache retrieved secrets
    _cache = {}

    @staticmethod
    def get_maps_api_key() -> str:
        cache_key = "GOOGLE_MAPS_API_KEY"

        # Consult the cache to prevent redundant API latency
        if cache_key in VaultService._cache:
            return VaultService._cache[cache_key]

        # Instantiate the official Google Cloud Secret Manager client
        client = secretmanager.SecretManagerServiceClient()

        # Construct the fully qualified resource name
        name = f"projects/{GCPConfig.PROJECT_ID}/secrets/{cache_key}/versions/latest"

        try:
            # Execute the secure retrieval request
            response = client.access_secret_version(request={"name": name})
            secret_payload = response.payload.data.decode("UTF-8")

            # Persist the payload in the local cache
            VaultService._cache[cache_key] = secret_payload
            return secret_payload

        except Exception as e:
            print(f"Vault Security Exception: {e}")
            return None
