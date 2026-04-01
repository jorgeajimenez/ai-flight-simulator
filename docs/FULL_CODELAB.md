# 🚀 Codelab: Build the Infinite Flight Persistent World

Welcome to the official GDG "Build with AI" Workshop. In this codelab, you will deconstruct a monolithic 3D flight simulator and rebuild its brain using the **Essential 6 Google Cloud Stack**.

## 🧠 The Curriculum

1.  **[Module 1: Cloud Setup & The Icebreaker](./01-cloud-setup.md)**
    *   Auth, Project Creation, and generating your first Imagen 3 texture.
2.  **[Module 2: Modular Architecture](./02-modular-architecture.md)**
    *   Implementing Service-Oriented Design and Zero-Trust with Secret Manager.
3.  **[Module 3: The Geospatial Engine](./03-geospatial-engine.md)**
    *   Using Google Earth Engine to fetch real-world satellite data.
4.  **[Module 4: Grounded Multimodal Vision](./04-ai-vision.md)**
    *   Building a **Visual RAG** pipeline with Gemini 2.5 Flash and Imagen 3.
5.  **[Module 5: Immersive Audio Engine](./05-immersive-audio.md)**
    *   Synthesizing lifelike pilot advisories with Cloud Text-to-Speech.
6.  **[Module 6: Agentic Intelligence & The Anomaly Tracker](./06-persistent-world.md)**
    *   **The Grand Finale:** Building an autonomous Agent using Vertex AI Function Calling (ADK) to scan the Persistent World.

## 🛠 Prerequisites
*   A Google Cloud Project with Billing enabled.
*   Access to Google Cloud Shell.
*   A "Build with AI" mindset.

Let's take flight. Get started with **[Module 1](./01-cloud-setup.md)**.
# Module 1: Cloud Setup & Initial Generation

Before building the flight simulator's brain, we need to ensure your environment is correctly wired to Google Cloud. If you are using a brand new Google account, follow these steps very carefully.

## Step 1: Account Preparation & Billing

1.  **Billing Account:** You must have an active billing account. Go to the [Google Cloud Billing Console](https://console.cloud.google.com/billing) and ensure a billing account is linked to your current project.
2.  **Activate Cloud Shell:** Click the `>_` terminal icon in the top right of your Google Cloud Console. This is your primary development environment.
3.  **Google Maps Platform:** 
    *   In the Cloud Console search bar, type "Google Maps Platform Credentials".
    *   Click **Create Credentials** -> **API Key** and copy it. You will need this in a moment.
    *   *(Note: The Photorealistic 3D Tiles API must be enabled for this key).*

<br><span style="color:red; font-weight:bold;">📸 TAKE SCREENSHOT: Your Google Cloud Console showing the APIs/Credentials screen. Save as `assets/dummy_enable_apis.png` to replace the placeholder!</span>

## Step 2: Clone & Configure

Run these commands in your Cloud Shell terminal to download the project and install dependencies:

```bash
git clone https://github.com/jorgeajimenez/ai-flight-simulator.git
cd ai-flight-simulator
uv sync
```

We've provided a setup script that creates your Service Account, enables necessary APIs (Vertex AI, Earth Engine, Secret Manager, TTS), and securely stores your Maps API key. Run it now:

```bash
bash scripts/setup_gcp.sh
```
*When prompted, paste your Google Maps API Key. The script will securely lock it inside Google Cloud Secret Manager.*

<br><span style="color:red; font-weight:bold;">📸 TAKE SCREENSHOT: Open 'Secret Manager' in your GCP Console UI and screenshot the `GOOGLE_MAPS_API_KEY` table. Save as `assets/dummy_secret_manager.png` to replace the placeholder!</span>

## Step 3: Earth Engine Registration (CRITICAL)
If you have a new Google Cloud account, you **must** manually accept the Earth Engine Terms of Service before the API will work, even if the script enabled it. 

1. Visit **[earthengine.google.com/signup](https://earthengine.google.com/signup)**
2. Ensure you are logged in with the correct Google account.
3. Click "Register" and accept the terms. If you skip this, your simulator will fail with a `403 Forbidden` error later.

---

## Step 4: Generate Base Texture

Before touching the backend code, let's test that your Vertex AI connection is working. We will use **Gemini 2.5 Flash** to generate a custom 3D building texture that will be used throughout the simulator.

Run the texture generation script:
```bash
uv run python scripts/generate_texture.py "Cyberpunk hacker apartment block..."
```

**Verification:**
If successful, the script will output `Saved texture to assets/texture.svg`. You can click on the `assets/texture.svg` file in the Cloud Shell editor to verify the image was generated. 

---

## Architecture: The Cloud Handshake

The diagram below shows how your Cloud Shell environment is communicating with Vertex AI using the credentials we just generated.

![Architecture: Cloud Handshake](./assets/01_cloud_setup.png)

*Notice how `uv` authenticates via the `service-account-key.json` file we generated in the setup script. This establishes a secure, zero-trust handshake with the Vertex AI API, allowing Gemini 2.5 Flash to generate our initial SVG texture and save it locally to the assets folder. This fundamental auth flow will power the rest of our AI services.*# Module 2: Enterprise Modular Architecture & TDD

This module refactors our application into an enterprise-grade Service-Oriented Architecture (SOA). We will also adopt a **Test-Driven Development (TDD)** workflow to ensure the AI application is robust.

## The "Essential 6" Stack

To scale this simulator, the backend has been deconstructed into six specialized services.

![Architecture: Modular SOA](./assets/02_modular_architecture.png)

*As seen in the diagram above, `app.py` acts as a central orchestrator. Instead of containing all the business logic, it delegates tasks to specialized modules. This prevents the "monolith" anti-pattern and makes it easy to swap out services.*

Each service has a single responsibility and is isolated for maximum testability:

1.  **Service 0 (Config):** Environment detection and logging initialization.
2.  **Service 1 (Vault):** Zero-trust secret management (Secret Manager) with in-memory caching for performance (e.g., `get_maps_api_key`).
3.  **Service 2 (Geospatial):** Real-time satellite fetching (Earth Engine).
4.  **Service 3 (AI Vision):** Multi-stage generative pipeline (Gemini + Imagen).
5.  **Service 4 (Audio):** Immersive Pilot voice synthesis (Text-to-Speech).
6.  **Service 5 (State Sync):** Shared Persistent World persistence (Firestore).

---

## The TDD Workflow

We don't just write code; we write specifications first. Our workflow for each service follows these steps:

1.  **Mocking the Cloud:** Since we don't want to make expensive API calls during every test run, we use `pytest-mock` to simulate Google Cloud responses.
2.  **Red Phase (Fail):** Write a test in the `tests/` directory that defines the expected output.
3.  **Green Phase (Pass):** Implement the minimal logic in the `services/` folder to satisfy the test.
4.  **Refactor:** Clean up the code while ensuring the tests stay green.

### Example: The Vault Service Test
We mock the `SecretManagerServiceClient` to ensure our backend handles network timeouts and fallbacks correctly without ever actually hitting the network. We also ensure our in-memory cache prevents redundant API calls.

```python
def test_get_maps_api_key_from_secret_manager(mocker):
    # Mock the Cloud SDK
    mock_client = MagicMock()
    mocker.patch("google.cloud.secretmanager.SecretManagerServiceClient", return_value=mock_client)
    
    # Simulate a successful response
    mock_response = MagicMock()
    mock_response.payload.data = b"cloud-secret-key"
    mock_client.access_secret_version.return_value = mock_response
    
    key = VaultService.get_maps_api_key()
    assert key == "cloud-secret-key"
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
Before we can test our newly unlocked `VaultService`, our Flask backend needs routes that the frontend can call. In the starter code, `app.py` only has the basic `/` index route. 

**[CODELAB ORCHESTRATION]** Open `app.py` and paste the following two API endpoints over the `TODO` marker. Notice how clean these routes are; they simply delegate all the heavy lifting to the AI services we are about to build!

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

<br><span style="color:red; font-weight:bold;">📸 TAKE SCREENSHOT: The Cloud Shell 'Web Preview' dropdown menu. Save as `assets/dummy_web_preview.png` to replace the placeholder!</span>

![Screenshot: Cloud Shell Web Preview button](./assets/dummy_web_preview.png)

*The Web Preview feature securely tunnels port 8080 from your Cloud Shell virtual machine directly to your browser. If you don't see the CesiumJS globe, double-check that your `service-account-key.json` is in the root directory and that the Flask server output doesn't show any startup errors.*

You should now see the 3D globe load successfully! The AI terraforming features won't work yet, but you can fly around the world. Keep the server running and open a **new terminal tab** for the next modules.

<br><span style="color:red; font-weight:bold;">📸 TAKE SCREENSHOT: The initial 3D globe loaded in the browser. Save as `assets/intro_screenshot.png` to replace the placeholder!</span># Module 3: The Geospatial Engine (Grounded Vision)

To create a believable 3D world, we need to base our AI textures on real-world geography. In this module, we will implement **Service 2: The Geospatial Engine** to fetch high-resolution satellite imagery from **Google Earth Engine**.

## Grounding the AI
A major challenge with Generative AI is "hallucination." If we just ask an AI to "draw Tokyo," it might get the buildings right but the street layout wrong. By fetching a real satellite image first, we **ground** the AI, forcing it to repaint over the real physical footprint of the city.

![Architecture: Geospatial Pipeline](./assets/03_geospatial_engine.png)

## Why Earth Engine?
While standard map APIs provide tiles for navigation, **Google Earth Engine** provides programmatic access to petabytes of scientific satellite data (like Sentinel-2). This allows us to fetch the raw data we need to feed our generative AI "terraforming" pipeline.

## Implementation: The `EarthEngineClient`

We encapsulate the complex Earth Engine SDK logic into a clean `fetch_satellite_tile` method. Before we can query the data, we must initialize the client explicitly using the project quota.

### Initialization (`services/geospatial.py`)
```python
# Explicitly request the Earth Engine scope and force the Project ID
credentials, _ = google.auth.default(scopes=[
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/earthengine"
])

# Force the credentials to use the specific project quota
if hasattr(credentials, "with_quota_project"):
    credentials = credentials.with_quota_project(GCPConfig.PROJECT_ID)
    
ee.Initialize(credentials=credentials, project=GCPConfig.PROJECT_ID)
```

### Fetching the Tile
The `fetch_satellite_tile` method performs three critical steps:
1.  **Calculate bounding box:** Defines the 500m x 500m area based on the pilot's coordinates.
2.  **Dataset Filtering:** Queries the `COPERNICUS/S2_SR_HARMONIZED` collection, filtering for the clearest (least cloudy) images.
3.  **Tile Extraction:** Downloads and returns the raw bytes.

```python
@staticmethod
def fetch_satellite_tile(lat: float, lon: float, offset: float = 0.0025) -> Tuple[bytes, List[float]]:
    # 1. Calculate bounding box
    area = ee.Geometry.Rectangle([lon - offset, lat - offset, lon + offset, lat + offset])
    
    # 2. Filter for the clearest satellite image
    collection = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                 .filterBounds(area)
                 .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
                 .sort('system:time_start', False))

    # 3. Process image and generate a download URL
    image = collection.first().select(['B4', 'B3', 'B2'])
    thumb_url = image.getThumbURL({'region': area, 'dimensions': 512, 'format': 'png', 'min': 0, 'max': 3000})
    
    # 4. Download and return the raw bytes
    response = requests.get(thumb_url)
    return response.content, [lat - offset, lon - offset, lat + offset, lon + offset]
```

## AI Wiring Point

In our main `app.py`, we can now "wire up" the geospatial engine with a single line of code:

```python
# AI_WIRING_POINT: Geospatial Fetch
image_bytes, bounds = EarthEngineClient.fetch_satellite_tile(lat, lon)
```

By isolating this logic, we keep our main application logic focused purely on orchestration.

---

## 🛠 Troubleshooting Earth Engine

If your server crashes when attempting to fetch the tile, check the following:

*   **`403 Forbidden` / User Not Registered:** If you are using a new Google account, you must explicitly accept the terms of service. Visit **[earthengine.google.com/signup](https://earthengine.google.com/signup)** and click "Register", then restart your server.
*   **API Not Enabled:** Ensure the Earth Engine API is actually enabled in your GCP Console. The `setup_gcp.sh` script should have done this, but quotas can occasionally delay activation.# Module 4: Multimodal AI Vision (Grounded Terraforming)

This is the most advanced part of the simulator's brain. In this module, we will build a **Visual RAG** pipeline. We don't just generate a random image; we use **Google Earth Engine** data to ground our generation in the real world.

The `AIVisionService` acts as our multimodal intelligence hub, providing two key functions:
1.  `describe_location`: Generating short pilot advisories about their current global position.
2.  `analyze_and_terraform`: A complex 2-stage generative pipeline for transforming the terrain.

## The 2-Stage Terraforming Loop

1.  **Stage 1: The Analyst (Gemini 2.5 Flash):** We send the raw satellite bytes to Gemini along with the pilot's prompt. Gemini analyzes the terrain and engineers a *technical* prompt for the image generator, returning a structured JSON response containing the prompt and a pilot advisory.
2.  **Stage 2: The Painter (Imagen 3):** We pass the engineered technical prompt and the *original* image to Imagen 3 (`imagen-3.0-generate-001`). Using image-to-image translation, Imagen "repaints" the world while keeping every street and building footprint exactly where they are in reality.

---

## Architecture: Visual RAG Sequence
This diagram shows how we move from a 1D text prompt to a 2D geographically grounded texture.

![Architecture: AI Vision Pipeline](./assets/04_ai_vision.png)

---

## Implementation: `AIVisionService`

Open `services/ai_vision.py` and find **[CODELAB STEP 3B]**. You will use the Gemini CLI to implement the following within `analyze_and_terraform`:

```python
# [CODELAB STEP 3B]
# 1. Stage 1: Initialize gemini-2.5-flash
# 2. Create a 'Part' from the satellite bytes
# 3. Request strict JSON output containing 'advisory' and 'imagen_prompt'
# 4. Stage 2: Initialize imagen-3.0-generate-001
# 5. Call edit_image with the base_image and engineered prompt
```

<br><span style="color:red; font-weight:bold;">📸 TAKE SCREENSHOT: Terraform a city (e.g., Cyberpunk) and capture the result! Save as `assets/03_cyberpunk_city.png`</span>
<br><span style="color:red; font-weight:bold;">📸 TAKE SCREENSHOT: Terraform 4 times in a row to trigger the memory limit. Capture the red "EVICTING OLD PATCH" toast notification! Save as `assets/04_memory_eviction.png`</span>

---

## 🛠 Troubleshooting AI Quotas

If you are using a new Google Cloud account, you might run into quota limitations:

*   **`429 Quota Exceeded`:** Vertex AI image generation limits are strict on fresh billing accounts. If the image fails to generate, wait a minute and try clicking the Terraform button again. 
*   **"API Not Enabled":** If `imagen` or `gemini` throws an unauthorized error, verify that the **Vertex AI API** is enabled in your Google Cloud Console.# Module 5: Immersive Audio (Text-to-Speech)

A flight simulator is not complete without an immersive audio experience. In this module, we will implement **Service 4: The Immersive Audio Engine** to turn Gemini's text advisories into a high-quality human voice.

## Multi-Voice Immersion
We are using **Cloud Text-to-Speech** to bring our AI entities to life. To differentiate between the Pilot and the Control Tower (ATC), our service accepts a `voice_type` parameter to select distinct, high-fidelity voice models:

*   **The Pilot (`voice_type="pilot"`):** Uses `en-US-Studio-O` for extremely natural, smooth briefings.
*   **The ATC (`voice_type="atc"`):** Uses `en-US-Journey-D` for an authoritative, "command-center" tone.

![Architecture: Audio Engine](./assets/05_immersive_audio.png)

## Implementation: `AudioSynthesisService`

We encapsulate the TTS logic into a single `synthesize_advisory` method. 

1.  **Request:** It sends the text to the Google Cloud TTS API.
2.  **Configuration:** It dynamically requests the correct voice model based on the `voice_type` parameter and specifies MP3 encoding.
3.  **Transmission:** It returns the audio data as a **Base64 encoded string**. This allows the frontend to play the audio instantly using the standard Web Audio API without needing to manage temporary files or additional requests.

### The Service Logic (`services/audio_engine.py`)

```python
@staticmethod
def synthesize_advisory(text: str, voice_type: str = "pilot") -> str:
    client = texttospeech.TextToSpeechClient()
    
    # Configure the voice based on the requested persona
    voice_name = "en-US-Journey-D" if voice_type == "atc" else "en-US-Studio-O"
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", name=voice_name)
    
    # Request MP3 format
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    
    response = client.synthesize_speech(
        input=texttospeech.SynthesisInput(text=text), 
        voice=voice, 
        audio_config=audio_config
    )
    
    # Return base64 encoded bytes
    return base64.b64encode(response.audio_content).decode('utf-8')
```

## AI Wiring Point

In our main `app.py`, we wire up the audio engine immediately after the AI Vision analysis for pilot advisories:

```python
# AI_WIRING_POINT: Immersive Audio Synthesis
audio_b64 = AudioSynthesisService.synthesize_advisory(ai_result['advisory'], voice_type="pilot")
```

Now, every time the world is terraformed, the pilot will hear a real-time vocal briefing!# Module 6: Agentic Intelligence & The Anomaly Tracker

In this final module, we move beyond simple APIs and build a true **Autonomous Agent** alongside a **Persistent World State Sync** service to share terraforming events globally.

## The Persistent World Client
Before we build the agent, we need a way to store and retrieve global events. The `PersistentWorldClient` handles this using two Cloud services:
1.  **Cloud Storage (Texture CDN):** When a user terraforms an area, the generated image is uploaded to a public Cloud Storage bucket. This acts as a global CDN for our textures.
2.  **Cloud Firestore (Metadata & Anomaly Tracker):** We store the metadata (latitude, longitude, prompt, and the public CDN URL) in Firestore. This creates a real-time database of all anomalies across the Persistent World.

## Why an Agent?
Instead of hardcoding what the "WHERE AM I?" button does, we give Gemini 2.5 Flash access to **Tools** via Vertex AI Function Calling (ADK). The `ControlTowerAgent` will autonomously decide to:
1.  **Visually identify** the landmark below the pilot using the `get_telemetry` tool.
2.  **Scan the Firestore database** using the `scan_anomaly_tracker` tool to find recent terraforming "anomalies" created by other pilots globally.

The Agent executes these tools in **parallel**, reads the data, and synthesizes a single, immersive audio advisory.

---

## Architecture: Parallel ADK Loop
This diagram shows how the Agent orchestrates other Cloud services as tools.

![Architecture: Persistent World Agent](./assets/06_persistent_world.png)

---

## Implementation: `ControlTowerAgent`

Open `services/control_tower.py` and find **[CODELAB STEP 6]**. You will build an Agent that:
*   Defines `get_telemetry` and `scan_anomaly_tracker` as `FunctionDeclaration` objects.
*   Passes these to the `GenerativeModel` as a `Tool`.
*   Uses `agent.start_chat()` to begin an agentic session.
*   Handles the `function_calls` loop to execute the logic in `ai_vision.py` and `state_sync.py`.

---

## Mission Accomplished! 🚀

You have successfully built an enterprise-grade **Service-Oriented Architecture** using the **Essential 6 Google Cloud Stack**. 

By mastering **Visual RAG**, **Function Calling**, and **Global State Sync**, you've proven that you can build AI systems that are grounded in reality and autonomous in action. 

**Capturing the Money Shot:**
1.  Terraform an area into "Mars Colony".
2.  Fly to a different city.
3.  Click "WHERE AM I?" and listen as your Agentic Control Tower warns you about the anomaly you just created in the Persistent World.

---

## 🛠 Troubleshooting Firestore

If you get a database error when saving or scanning the anomaly tracker:

*   **Firestore Initialization:** New Google Cloud projects do not have a database initialized by default. Go to the **Firestore** section in the Google Cloud Console. If prompted, click **Create Database** and ensure you select **Native Mode**. The `setup_gcp.sh` script attempts to create this, but it may require manual confirmation on a brand new billing account.

<br><span style="color:red; font-weight:bold;">📸 TAKE SCREENSHOT: The Firestore setup wizard showing 'Native Mode' selected. Save as `assets/dummy_firestore.png` to replace the placeholder!</span>