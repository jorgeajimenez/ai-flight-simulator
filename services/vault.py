import os
from google.cloud import secretmanager
from config import GCPConfig

class VaultService:
    # Initialize an in-memory variable to cache retrieved secrets
    _api_key_cache = None

    @staticmethod
    def get_maps_api_key() -> str:
        cache_key = "GOOGLE_MAPS_API_KEY"

        # Consult the cache to prevent redundant API latency
        if VaultService._api_key_cache:
            return VaultService._api_key_cache

        try:
            # Instantiate the official Google Cloud Secret Manager client
            client = secretmanager.SecretManagerServiceClient()

            # Construct the fully qualified resource name
            name = f"projects/{GCPConfig.PROJECT_ID}/secrets/{cache_key}/versions/latest"

            # Execute the secure retrieval request
            response = client.access_secret_version(request={"name": name})
            secret_payload = response.payload.data.decode("UTF-8")

            # Persist the payload in the local cache
            VaultService._api_key_cache = secret_payload
            return secret_payload

        except Exception as e:
            print(f"Vault Security Exception: {e}")
            # Fallback to environment variable as defined in our tests
            return os.environ.get("GOOGLE_MAPS_API_KEY")
