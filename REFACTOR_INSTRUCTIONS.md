# Refactor Instructions: The Essential 6 Service-Oriented Architecture (Test-Driven)

## Objective
Deconstruct the `app.py` monolith into an enterprise-grade, modular backend using a **Test-Driven Development (TDD)** approach. This architecture is designed to be "Seamless," "AI-Wirable," and strictly utilizes the **Essential 6 Google Cloud Stack** to deliver a persistent 3D generative world. 

The goal is to build out the tests first, verify the architecture, and then implement the modular codebase with clear `TODO` markers where the actual codelab attendees will "wire up" the Google Cloud services.

---

## 1. Modular Directory Blueprint
The refactor must strictly follow this structure to ensure reusability, testability, and clear separation of concerns.

```text
infinite-loop-simulator/
├── requirements.txt           # Must include pytest, pytest-mock for TDD
├── app.py                     # Entry point: Flask App Orchestration (< 50 lines)
├── config.py                  # Service 0: Environment & GCP Config (Cloud Run Optimized)
├── services/
│   ├── __init__.py
│   ├── ai_vision.py           # Service 1: Vertex AI (Gemini 1.5 Flash + Imagen 3)
│   ├── geospatial.py          # Service 2: Google Earth Engine (Satellite Fetching)
│   ├── audio_engine.py        # Service 3: Cloud Text-to-Speech (Studio Voice Engine)
│   ├── state_sync.py          # Service 4: Firestore (Real-time Persistent World Persistence)
│   └── vault.py               # Service 5: Secret Manager (Zero-Trust Key Management)
└── tests/                     # TDD Test Suite
    ├── __init__.py
    ├── test_app.py
    ├── test_ai_vision.py
    ├── test_geospatial.py
    ├── test_audio_engine.py
    ├── test_state_sync.py
    └── test_vault.py
```

---

## 2. Current State Analysis & Migration Plan
Based on the existing `app.py`, here is the direct migration path for the refactor:

1. **Extract `config.py`:** Move the hardcoded `PROJECT_ID`, `LOCATION`, and credential logic from lines 19-24.
2. **Deconstruct `init_ai_services()`:** Split lines 26-44. Earth Engine initialization moves to `services/geospatial.py`, Vertex AI initialization moves to `services/ai_vision.py`.
3. **Extract `services/vault.py`:** Move the `os.environ.get('GOOGLE_MAPS_API_KEY')` logic from the index route and upgrade it to query Secret Manager.
4. **Extract `services/geospatial.py`:** Move the `COPERNICUS/S2_SR_HARMONIZED` filtering and `ThumbURL` generation from the `/terraform` route.
5. **Extract `services/ai_vision.py`:** Move the `ImageGenerationModel` terraforming logic out of the `/terraform` route.
6. **Net-New Implementations:** The current baseline lacks Gemini 1.5 Flash analysis, Text-to-Speech, and Firestore. These will be built from scratch as `services/audio_engine.py` and `services/state_sync.py`, and Gemini will be added to `ai_vision.py`.

---

## 3. Test-Driven Development (TDD) Mandates
Before implementing the service logic, write comprehensive unit tests using `pytest` and `pytest-mock`.
- **Mock External Calls:** Every call to a Google Cloud API (Vertex AI, Earth Engine, Secret Manager, Firestore, TTS) must be mocked in the test suite. No test should make a real network request.
- **Test App Routes:** The `/terraform` route in `app.py` must be tested using a mocked Flask test client to ensure all services are orchestrated correctly.
- **Fail Fast:** The tests should define the exact expected behavior and JSON schemas before the actual service implementations are filled in.

---

## 4. Service Implementation Mandates (The Codelab Target)

### Task 0: Configuration (`config.py`)
- **Mandate:** Implement a `GCPConfig` class detecting `GOOGLE_CLOUD_PROJECT`.
- **Pattern:** Use standard Python `logging` configured for Cloud Logging compatibility.

### Task 1: Secret Operations (`services/vault.py`)
- **Cloud Service:** **Secret Manager** (`secretmanager.googleapis.com`).
- **AI-Wirable Pattern:** Implement `get_maps_api_key()` with an in-memory cache.

### Task 2: Geospatial Engine (`services/geospatial.py`)
- **Cloud Service:** **Google Earth Engine** (`earthengine.googleapis.com`).
- **Method:** `fetch_satellite_tile(lat, lon, offset=0.0025)` returning raw bytes.

### Task 3: Multimodal Intelligence (`services/ai_vision.py`)
- **Cloud Service:** **Vertex AI** (`aiplatform.googleapis.com`).
- **Method:** `analyze_and_terraform(image_bytes, user_prompt)`.
- **Strict Logic:** 
    - Use Gemini 1.5 Flash with `response_mime_type: "application/json"` to generate `{"advisory": string, "imagen_prompt": string}`.
    - Use Imagen 3 (`imagegeneration@006`) to perform image-to-image transformation.

### Task 4: Immersive Audio Engine (`services/audio_engine.py`)
- **Cloud Service:** **Cloud Text-to-Speech** (`texttospeech.googleapis.com`).
- **Method:** `synthesize_advisory(text)` using the `en-US-Studio-O` voice, returning Base64 MP3 bytes.

### Task 5: Persistent World State Sync (`services/state_sync.py`)
- **Cloud Service:** **Firestore** (`firestore.googleapis.com`).
- **Method:** `log_terraform_event(lat, lon, prompt)`.

### Task 6: Routing Orchestration (`app.py`)
- **Source-to-Run:** `app.py` must use the services to process the POST request sequentially.
- **Web Console Compatibility:** Include machine-readable comments (`# AI_WIRING_POINT`) at the integration points in `app.py` to guide the Gemini CLI and codelab attendees during the final assembly.

---

## 5. Evaluation Criteria
An implementation is successful if:
1. Running `pytest tests/` passes with 100% success on the mocked architecture.
2. `app.py` is reduced to < 50 lines of purely routing logic.
3. Every cloud service call is strictly isolated in its respective `services/` file.
4. The codebase is prepared to be cloned out as starter code for the codelab (with the actual API calls stubbed out or marked for implementation).
