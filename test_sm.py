import os
from google.cloud import secretmanager
from config import GCPConfig

print(f"Project ID: {GCPConfig.PROJECT_ID}")
try:
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{GCPConfig.PROJECT_ID}/secrets/GOOGLE_MAPS_API_KEY/versions/latest"
    print(f"Attempting to access: {name}")
    response = client.access_secret_version(request={"name": name})
    print("Success!")
except Exception as e:
    print(f"FAILED WITH EXCEPTION: {type(e).__name__}")
    print(str(e))
