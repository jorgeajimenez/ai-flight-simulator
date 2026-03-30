from google.cloud import firestore, storage
from config import GCPConfig, logger
import hashlib
import base64

class GlobalMultiverseClient:
    """
    Multiverse State Sync powered by Cloud Firestore and Cloud Storage.
    Persists terraforming events and acts as a Global Texture CDN.
    """
    
    @staticmethod
    def get_recent_activity(lat: float, lon: float) -> list:
        """
        Reads the most recent terraforming anomalies from Firestore.
        This acts as the 'Radar' for the ATC Agent.
        """
        try:
            logger.info("State Sync: Agent scanning multiverse activity...")
            db = firestore.Client(project=GCPConfig.PROJECT_ID)
            
            # Fetch the 3 most recent terraforming events globally
            docs = db.collection("terraforms").order_by(
                "timestamp", direction=firestore.Query.DESCENDING
            ).limit(3).stream()
            
            results = []
            for doc in docs:
                data = doc.to_dict()
                results.append(f"Anomaly: '{data.get('prompt')}' detected at Lat {data.get('latitude'):.2f}, Lon {data.get('longitude'):.2f}")
                
            return results
        except Exception as e:
            logger.error(f"State Sync Read Error: {e}")
            return ["Unable to scan multiverse database."]

    @staticmethod
    def log_terraform_event(lat: float, lon: float, prompt: str, image_b64: str) -> str:
        """
        Uploads the generated texture to Cloud Storage (CDN) and saves the metadata to Firestore.
        Returns the public URL of the uploaded texture.
        """
        try:
            logger.info(f"State Sync: Persisting '{prompt}' anomaly at {lat}, {lon}...")
            
            # 1. Upload Texture to Cloud Storage (The CDN)
            storage_client = storage.Client(project=GCPConfig.PROJECT_ID)
            # Create a deterministic bucket name based on the project ID
            bucket_name = f"{GCPConfig.PROJECT_ID}-multiverse-textures"
            
            try:
                bucket = storage_client.get_bucket(bucket_name)
            except Exception:
                # Create the bucket if it doesn't exist (in a real app, do this in Terraform/setup)
                logger.info(f"State Sync: Creating new storage bucket '{bucket_name}'...")
                bucket = storage_client.create_bucket(bucket_name, location=GCPConfig.LOCATION)
                # Make the bucket publicly readable
                policy = bucket.get_iam_policy(requested_policy_version=3)
                policy.bindings.append({"role": "roles/storage.objectViewer", "members": {"allUsers"}})
                bucket.set_iam_policy(policy)

            # Generate a unique hash for the file name based on coords and prompt
            file_hash = hashlib.md5(f"{lat}-{lon}-{prompt}".encode()).hexdigest()[:12]
            blob = bucket.blob(f"textures/{file_hash}.png")
            
            # Decode the base64 string back to bytes and upload
            image_bytes = base64.b64decode(image_b64)
            blob.upload_from_string(image_bytes, content_type="image/png")
            
            texture_url = blob.public_url
            logger.info(f"State Sync: Texture cached at {texture_url}")

            # 2. Persist Metadata to Firestore
            db = firestore.Client(project=GCPConfig.PROJECT_ID)
            event_data = {
                "latitude": lat,
                "longitude": lon,
                "prompt": prompt,
                "texture_url": texture_url,
                "timestamp": firestore.SERVER_TIMESTAMP
            }
            db.collection("terraforms").add(event_data)
            
            return texture_url
            
        except Exception as e:
            logger.error(f"State Sync Write Error: {e}")
            return ""
