# Module 2: Enterprise Modular Architecture & TDD

In this module, we transition from a monolithic "script" to an enterprise-grade Service-Oriented Architecture (SOA). We will also adopt a **Test-Driven Development (TDD)** workflow to ensure our AI application is robust and "re-buildable."

## The "Essential 6" Stack

To scale this simulator, we've deconstructed the backend into six specialized services.

![Architecture: Modular SOA](./assets/02_modular_architecture.png)

*As seen in the diagram above, our `app.py` acts as a central orchestrator. Instead of containing all the business logic, it delegates tasks to specialized modules. This prevents the "monolith" anti-pattern and makes it incredibly easy to swap out services (like changing our TTS provider or database) without breaking the entire application.*

Each service has a single responsibility and is isolated for maximum testability:

1.  **Service 0 (Config):** Environment detection and logging initialization.
2.  **Service 1 (Vault):** Zero-trust secret management (Secret Manager) with in-memory caching for performance (e.g., `get_maps_api_key`).
3.  **Service 2 (Geospatial):** Real-time satellite fetching (Earth Engine).
4.  **Service 3 (AI Vision):** Multi-stage generative pipeline (Gemini + Imagen).
5.  **Service 4 (Audio):** Immersive Pilot voice synthesis (Text-to-Speech).
6.  **Service 5 (State Sync):** Shared Persistent World persistence (Firestore).

---

## The TDD Workflow (Red-Green-Refactor)

In cloud engineering, TDD is paramount. Executing full integration tests against live generative AI endpoints for every code iteration introduces latency and unintended API consumption. 

To circumvent this, we use `pytest-mock` to simulate Google Cloud responses locally.

**Action Marker 2.1:** Execute the test suite for the Vault Service. This execution will intentionally fail (the "Red" state) because the service is not yet implemented.

```bash
uv run pytest tests/test_vault.py
```

The terminal output will yield an `AssertionError`. To resolve this and transition to the "Green" state, you must implement the Vault Service.

**Action Marker 2.2:** Open `services/vault.py` and paste the following implementation. This code integrates an in-memory cache to minimize redundant network calls, and an environment variable fallback, perfectly satisfying our tests.

```python
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

        # Instantiate the official Google Cloud Secret Manager client
        client = secretmanager.SecretManagerServiceClient()

        # Construct the fully qualified resource name
        name = f"projects/{GCPConfig.PROJECT_ID}/secrets/{cache_key}/versions/latest"

        try:
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
```

**Action Marker 2.3:** Re-execute the test suite. The terminal should now indicate `3 passed` (the "Green" state).

```bash
uv run pytest tests/test_vault.py
```

## Directory Blueprint

By the end of this refactor, your project structure will look like this:

```text
infinite-loop-simulator/
├── app.py                # The Orchestrator (< 50 lines)
├── config.py             # Service 0: GCP Configuration
├── services/             # The Service Core
│   ├── vault.py          # Service 1: Secret Management
│   ├── geospatial.py     # Service 2: Earth Engine
│   └── ...               # (Services 3-5)
└── tests/                # The TDD Suite
```

This structure makes the application **"AI-Wirable"**—meaning each service can be independently tested and easily integrated into the main application via standardized interfaces.

---

## 🔌 The Orchestrator (`app.py`)
Before we can test our newly unlocked `VaultService`, our Flask backend needs routes that the frontend can call. In the starter code, `app.py` only has the basic `/` index route and a `[CODELAB ORCHESTRATION]` placeholder block at the bottom.

**Instructions:** Open `app.py` in your editor and locate the `[CODELAB ORCHESTRATION]` block near the bottom. We are going to paste **two separate endpoints** into this space.

### Step 1: The Locate Endpoint
First, paste the `/locate` endpoint. This route handles the "WHERE AM I?" button click from the frontend. Notice how clean it is—it completely delegates the heavy lifting to the Agentic Control Tower and the Audio Synthesis engine.

```python
@app.route("/locate", methods=["POST"])
def locate():
    try:
        data = request.json
        lat, lon = data.get("lat"), data.get("lon")

        # 1. Ask the Agentic Control Tower
        atc_response = ControlTowerAgent.contact_tower(lat, lon)

        # 2. Synthesize the audio
        audio_b64 = AudioSynthesisService.synthesize_advisory(
            atc_response, voice_type="atc"
        )

        return jsonify({"audio": audio_b64, "text": atc_response})
    except Exception as e:
        logger.error(f"ATC Agent Error: {e}")
        return jsonify({"error": str(e)}), 500
```

### Step 2: The Terraform Endpoint
Next, immediately below the `/locate` route, paste the `/terraform` endpoint. This route is the heart of our simulator, chaining together 4 different cloud services sequentially to alter the physical world.

```python
@app.route("/terraform", methods=["POST"])
def terraform():
    try:
        data = request.json
        lat, lon, prompt = (
            data.get("lat"),
            data.get("lon"),
            data.get("prompt", "Cyberpunk City"),
        )

        # AI_WIRING_POINT: Service 2 (Geospatial)
        image_content, bounds = EarthEngineClient.fetch_satellite_tile(lat, lon)

        # AI_WIRING_POINT: Service 1 (Vision)
        ai_result = AIVisionService.analyze_and_terraform(image_content, prompt)

        # AI_WIRING_POINT: Service 3 (Audio)
        audio_b64 = AudioSynthesisService.synthesize_advisory(ai_result["advisory"])

        # AI_WIRING_POINT: Service 4 (Persistence & CDN)
        texture_url = PersistentWorldClient.log_terraform_event(
            lat, lon, prompt, ai_result["image_b64"]
        )

        return jsonify(
            {
                "image": ai_result["image_b64"],
                "audio": audio_b64,
                "narrative": ai_result["advisory"],
                "bounds": bounds,
                "texture_url": texture_url,
            }
        )
    except Exception as e:
        logger.error(f"Terraforming Error: {e}")
        return jsonify({"error": str(e)}), 500
```

---

## 🚀 Your First Flight: Test the Simulator!

Now that you've implemented the Vault Service using the Gemini CLI, the backend can finally pull the Google Maps API Key and serve it to the frontend. Let's test it!

1. Start the Flask server in your Cloud Shell terminal:
   ```bash
   uv run app.py
   ```
2. Click the **Web Preview** button (the eye icon) in the top right of your Cloud Shell.
3. Select **Preview on port 8080**.

![Screenshot: Cloud Shell Web Preview button](./assets/dummy_web_preview.png)

*The Web Preview feature securely tunnels port 8080 from your Cloud Shell virtual machine directly to your browser. If you don't see the CesiumJS globe, double-check that your `service-account-key.json` is in the root directory and that the Flask server output doesn't show any startup errors.*

You should now see the 3D globe load successfully! The AI terraforming features won't work yet, but you can fly around the world. Keep the server running and open a **new terminal tab** for the next modules.