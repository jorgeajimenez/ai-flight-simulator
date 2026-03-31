# 🧪 The Infinite Flight Persistent World: Dry Run Guide

**Purpose:** This document is your master control manual for the GDG event. 

**Part 1** is the Dry Run Guide: follow this *exactly* on a completely separate, fresh Google Cloud account to simulate the attendee experience and flush out any hidden "it works on my machine" bugs.
**Part 2** is the Teacher's Answer Key: keep this open during the workshop. If an attendee's Gemini CLI gets stuck or hallucinates, you can copy-paste the exact required code blocks from here.

---

## PART 1: THE DRY RUN (Simulating the Attendee)

### Step 1: The Incognito Clean Slate
You must use a secondary Google account (e.g., a personal Gmail) that has **never** run this project before.

1. Open an **Incognito / Private Browsing** window.
2. Log into Google with your **Test Account**.
3. Go to [console.cloud.google.com](https://console.cloud.google.com/).
4. **Billing Check:** Even test accounts need a billing account attached. Go to the Billing section and ensure one is active (e.g., the $300 free trial).
5. Click the **Activate Cloud Shell** icon (the terminal prompt `>_` in the top right corner).

---

### Step 2: Workspace Prep (Inside Cloud Shell)
Cloud Shell is an ephemeral Linux VM. We need to get the code and our package manager (`uv`) installed.

1. **Install `uv`:** Cloud Shell doesn't have `uv` by default. Run this to install it:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source $HOME/.local/bin/env
   ```

2. **Clone the Repository:**
   *(Note: If the repo is still private during your dry run, you will need to generate a GitHub Personal Access Token (PAT) to clone it here. For the actual event, the repo should be public).*
   ```bash
   git clone https://github.com/jorgeajimenez/ai-flight-simulator.git
   cd ai-flight-simulator
   git checkout code-lab-migration
   ```

---

### Step 3: Running the Automated Setup
Because Cloud Shell is pre-authenticated, the script will skip the login step and go straight to project creation.

1. Execute the setup script:
   ```bash
   bash setup_gcp.sh
   ```
2. **Follow the prompts:**
   - Create a unique project ID (e.g., `gdg-test-flight-001`).
   - Select the billing account ID.
   - When prompted for the Maps API Key, you can press Enter to skip for now, OR go grab a key from your test account's console.

---

### Step 4: The "Manual Magic" (Crucial Console Steps)
These are the steps the script *cannot* do for security/legal reasons. You must verify these work for a fresh account.

1. **Earth Engine Registration:**
   - Go to [earthengine.google.com/non-commercial/](https://earthengine.google.com/non-commercial/).
   - Register your test account for "Unpaid/Non-commercial" use.
   - *Teacher Note: If attendees skip this, the Geospatial API throws a 403 Forbidden error during terraforming.*

2. **Google Maps 3D Tiles Handshake:**
   - Go to the [Google Maps Platform Console](https://console.cloud.google.com/google/maps-apis/overview).
   - Click "Get Started" (if it's a new account, it might ask you to confirm billing details).
   - Search for **"Photorealistic 3D Tiles"** in the APIs library and click **Enable**.
   - Go to the "Credentials" tab, copy the API Key.

3. **Secret Manager (If skipped in Step 3):**
   - Go to [Secret Manager](https://console.cloud.google.com/security/secret-manager).
   - Create a secret named `GOOGLE_MAPS_API_KEY` and paste your key.

---

### Step 5: The Attendee Experience & Testing
Now, pretend to be the attendee following the Codelab.

1. Install Python dependencies:
   ```bash
   uv sync
   ```
2. **The Icebreaker Test:** Run the texture generator.
   ```bash
   uv run python generate_texture.py "glowing neon steampunk"
   ```
   *Did `assets/texture.svg` update?*
3. **The Codelab Loop:** Use the **Gemini CLI** to fill in the `TODO` markers in `services/vault.py`, `services/ai_vision.py`, etc., checking your work against Part 2 below.
4. Start the server:
   ```bash
   uv run python app.py
   ```
5. **The Web Preview Test:**
   - In the top right of the Cloud Shell terminal pane, click the **Web Preview** icon.
   - Click **Preview on port 8080**.
6. **The Final Verification Checklist:**
   - [ ] **Maps:** Do the 3D buildings load? 
   - [ ] **Terraform (Vision/Earth Engine/TTS):** Click "Transform Area". Does the audio play, and does the terrain change to a Cyberpunk city?
   **The Anomaly Tracker:** Fly somewhere else, click "WHERE AM I?". Does the ATC agent warn you about the anomaly you just created?

---

### Step 6: Teardown (Don't get billed!)
Once you are satisfied the dry run was successful, destroy the test project so your test account isn't charged.

```bash
gcloud projects delete gdg-test-flight-001
```

---
---

## PART 2: THE TEACHER's ANSWER KEY

If an attendee gets stuck, or their Gemini instance writes code that doesn't work, use these exact blocks to fix their `services/` files.

### Module 2: The Vault Service (`services/vault.py`)
**Goal:** Fetch the Google Maps API key from Secret Manager.

```python
# [CODELAB STEP 1]
client = secretmanager.SecretManagerServiceClient()
name = f"projects/{GCPConfig.PROJECT_ID}/secrets/{secret_id}/versions/latest"
response = client.access_secret_version(request={"name": name})

key = response.payload.data.decode("UTF-8")
cls._cache[secret_id] = key
return key
```

### Module 3: Geospatial Engine (`services/geospatial.py`)
**Goal:** Fetch Sentinel-2 Satellite imagery.

**[CODELAB STEP 2A] Earth Engine Init**
*Teacher Note: We explicitly define the scopes and force the project here. If an attendee uses `ee.Initialize()` without credentials, it will crash with a 403 or "Authenticate" error.*
```python
credentials, _ = google.auth.default(scopes=[
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/earthengine"
])
if hasattr(credentials, "with_quota_project"):
    credentials = credentials.with_quota_project(GCPConfig.PROJECT_ID)
    
ee.Initialize(credentials=credentials, project=GCPConfig.PROJECT_ID)
logger.info("Geospatial: Earth Engine Initialized.")
```

**[CODELAB STEP 2B] Satellite Fetch**
```python
area = ee.Geometry.Rectangle([min_lon, min_lat, max_lon, max_lat])

collection = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
             .filterBounds(area)
             .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
             .sort('system:time_start', False))

image = collection.first().select(['B4', 'B3', 'B2'])

thumb_url = image.getThumbURL({
    'region': area,
    'dimensions': 512,
    'format': 'png',
    'min': 0,
    'max': 3000
})

response = requests.get(thumb_url)
response.raise_for_status()

return response.content, [min_lat, min_lon, max_lat, max_lon]
```

### Module 4: Multimodal Vision (`services/ai_vision.py`)
**Goal:** Visual RAG pipeline with Gemini 2.5 Flash and Imagen 3.

**[CODELAB STEP 3A] SVG Texture Gen**
```python
gemini_model = GenerativeModel("gemini-2.5-flash")
res = gemini_model.generate_content(svg_prompt)

svg_code = res.text.strip()
if "```" in svg_code:
    svg_code = svg_code.split("```")[1].replace("svg", "", 1).strip()
    
return base64.b64encode(svg_code.encode('utf-8')).decode('utf-8')
```

**[CODELAB STEP 3B] Gemini Terraforming Analysis**
*Teacher Note: Ensure `response_mime_type` is present to enforce strict JSON output.*
```python
gemini_model = GenerativeModel("gemini-2.5-flash")
terrain_image = Part.from_data(data=image_bytes, mime_type="image/png")

gemini_res = gemini_model.generate_content(
    [terrain_image, gemini_prompt],
    generation_config={"response_mime_type": "application/json"}
)

ai_plan = json.loads(gemini_res.text.strip())
```

**[CODELAB STEP 3C] Imagen 3 Terraforming**
```python
imagen_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
base_image = VertexImage(image_bytes=image_bytes)

generated_images = imagen_model.edit_image(
    base_image=base_image, 
    prompt=ai_plan['imagen_prompt']
)

output_buffer = BytesIO()
generated_images[0].save(output_buffer, include_generation_parameters=False)
generated_img_b64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
```

### Module 5: Immersive Audio (`services/audio_engine.py`)
**Goal:** Generate lifelike voices for Pilot and ATC.

**[CODELAB STEP 4] Text-to-Speech**
```python
client = texttospeech.TextToSpeechClient()
synthesis_input = texttospeech.SynthesisInput(text=text)

# Journey for ATC, Studio for Pilot
voice_name = "en-US-Journey-D" if voice_type == "atc" else "en-US-Studio-O"

voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", 
    name=voice_name
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

response = client.synthesize_speech(
    input=synthesis_input, 
    voice=voice, 
    audio_config=audio_config
)

return base64.b64encode(response.audio_content).decode("utf-8")
```

### Module 6: Persistent World State Sync & Anomaly Tracker (`services/state_sync.py` & `control_tower.py`)
**Goal:** Global Texture CDN and the Agentic Radar loop.

**[CODELAB STEP 5A & 5B] Write State & Upload CDN (`state_sync.py`)**
```python
# 1. Cloud Storage Upload
storage_client = storage.Client(project=GCPConfig.PROJECT_ID)
bucket_name = f"{GCPConfig.PROJECT_ID}-persistent-textures"

try:
    bucket = storage_client.get_bucket(bucket_name)
except Exception:
    bucket = storage_client.create_bucket(bucket_name, location=GCPConfig.LOCATION)
    policy = bucket.get_iam_policy(requested_policy_version=3)
    policy.bindings.append({"role": "roles/storage.objectViewer", "members": {"allUsers"}})
    bucket.set_iam_policy(policy)

import hashlib
file_hash = hashlib.md5(f"{lat}-{lon}-{prompt}".encode()).hexdigest()[:12]
blob = bucket.blob(f"textures/{file_hash}.png")

image_bytes = base64.b64decode(image_b64)
blob.upload_from_string(image_bytes, content_type="image/png")
texture_url = blob.public_url

# 2. Firestore Metadata Save
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
```

**[CODELAB STEP 6A] Identify Landmark (`ai_vision.py`)**
```python
gemini_model = GenerativeModel("gemini-2.5-flash")
res = gemini_model.generate_content(prompt)
return res.text.strip()
```

**[CODELAB STEP 6B] Read Firestore Anomaly Tracker (`state_sync.py`)**
```python
db = firestore.Client(project=GCPConfig.PROJECT_ID)
docs = db.collection("terraforms").order_by(
    "timestamp", direction=firestore.Query.DESCENDING
).limit(3).stream()

results = []
for doc in docs:
    data = doc.to_dict()
    results.append(f"Anomaly: '{data.get('prompt')}' detected at Lat {data.get('latitude'):.2f}, Lon {data.get('longitude'):.2f}")
    
return results
```

**[CODELAB STEP 6C] Parallel Tool Calling Loop (`control_tower.py`)**
*Teacher Note: This is the most complex code in the lab. Ensure attendees get the parallel loop correct!*
```python
model_name = "gemini-2.5-flash"
agent = GenerativeModel(model_name, tools=[atc_tools])

chat = agent.start_chat()
response = chat.send_message(prompt)

# Handle Parallel Tool Calling Loop
if response.candidates and response.candidates[0].content.parts:
    function_responses = []
    
    for part in response.candidates[0].content.parts:
        if part.function_call:
            fn = part.function_call
            
            if fn.name == "get_telemetry":
                from services.ai_vision import AIVisionService
                location_desc = AIVisionService.describe_location(lat, lon)
                function_responses.append(
                    Part.from_function_response(name=fn.name, response={"content": {"weather": "Winds 12kt North.", "landmark": location_desc}})
                )
                
            elif fn.name == "scan_anomaly_tracker":
                from services.state_sync import PersistentWorldClient
                recent_anomalies = PersistentWorldClient.get_recent_activity(lat, lon)
                function_responses.append(
                    Part.from_function_response(name=fn.name, response={"content": {"recent_anomalies": recent_anomalies}})
                )
    
    # Return all results to the LLM at once
    if function_responses:
        response = chat.send_message(function_responses)
    
return response.text.replace("*", "").strip()
```
