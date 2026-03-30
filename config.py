import os
import logging
import subprocess
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# --- GDG INFINITE FLIGHT CONFIGURATION ---
# This module centralizes all GCP and Application settings.

# MAGIC FIX FOR LOCAL DEV: Auto-detect the service account key and Project ID
key_path = os.path.abspath("service-account-key.json")
project_from_key = None

if os.path.exists(key_path):
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
    try:
        with open(key_path, "r") as f:
            import json
            data = json.load(f)
            project_from_key = data.get("project_id")
            logging.info(f"Config: Detected Project ID from key file: {project_from_key}")
    except Exception as e:
        logging.warning(f"Config: Could not parse key file for project ID: {e}")

def get_active_gcloud_project() -> str:
    """Attempts to dynamically fetch the active gcloud project."""
    try:
        return subprocess.check_output(["gcloud", "config", "get-value", "project"]).decode("utf-8").strip()
    except Exception:
        return "your-project-id"

class GCPConfig:
    """
    Configuration Manager for Google Cloud Services.
    Forces the Service Account Key to be the absolute source of truth to prevent terminal pollution.
    """
    PROJECT_ID: str = project_from_key or os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("PROJECT_ID") or get_active_gcloud_project()
    LOCATION: str = os.environ.get("GOOGLE_CLOUD_LOCATION") or os.environ.get("LOCATION", "us-central1")

    @classmethod
    def validate(cls) -> None:
        """Validates that critical configuration is present."""
        if not cls.PROJECT_ID or cls.PROJECT_ID == "your-project-id":
            logging.warning("GCP Project ID is not set. Cloud services WILL fail.")
        else:
            logging.info(f"Configured for GCP Project: {cls.PROJECT_ID}")

# Configure standard Python logging for Cloud Run compatibility
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger("infinite-flight")

# AI_WIRING_POINT: Config Initialization
GCPConfig.validate()
