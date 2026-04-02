# 🧪 The Infinite Flight Persistent World: Dry Run Guide

**Purpose:** This document is your master control manual for the GDG event. 

**Part 1** is the Dry Run Guide: follow this *exactly* on a completely separate, fresh Google Cloud account to simulate the attendee experience and flush out any hidden "it works on my machine" bugs.
**Part 2** is the Teacher's Answer Key: keep this open during the workshop. If an attendee gets stuck, you can copy-paste the exact required code blocks from here.

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
Cloud Shell is an ephemeral Linux VM. We just need to get the code.

1. **Clone the Repository:**
   *(Note: If the repo is still private during your dry run, you will need to generate a GitHub Personal Access Token (PAT) to clone it here).*
   ```bash
   git clone --depth 1 -b solution-slim https://github.com/jorgeajimenez/ai-flight-simulator.git
   cd ai-flight-simulator
   ```

---

### Step 3: Running the Automated Setup
Because Cloud Shell is pre-authenticated, the script will skip the login step and go straight to project creation.

1. Execute the setup script:
   ```bash
   bash scripts/setup_gcp.sh
   ```
2. **Follow the prompts:**
   - Create a unique project ID (e.g., `gdg-test-flight-001`).
   - Select the billing account ID.
   - **Crucial:** Click the **STEP 1** and **STEP 2** links to manually enable the Map Tiles API and generate the Google Maps API key, then paste it back into the terminal.

---

### Step 4: The Attendee Experience & Testing
Now, pretend to be the attendee following the Codelab.

1. Install Python dependencies:
   ```bash
   uv sync
   ```
2. **The Codelab Loop:** Use the **Gemini CLI** to fill in the `tickets_v2.csv`, checking your work against Part 2 below.
3. Start the server:
   ```bash
   uv run python app.py
   ```
4. **The Web Preview Test:**
   - In the top right of the Cloud Shell terminal pane, click the **Web Preview** icon.
   - Click **Preview on port 8080**.
5. **The Final Verification Checklist:**
   - [ ] **Maps:** Do the 3D buildings load? 
   - [ ] **A2A Comms:** Click "WHERE AM I?". Does the audio play, and does the ATC agent tell you the correct local time using the ADK tool?
   - [ ] **Terraform (Vision/Imagen/TTS):** Type a prompt and click "Transform Area". Does the audio play, and does the terrain change to a procedurally generated biome?

---

### Step 5: Teardown (Don't get billed!)
Once you are satisfied the dry run was successful, destroy the test project so your test account isn't charged.

```bash
gcloud projects delete gdg-test-flight-001
```

---
---

## PART 2: THE TEACHER's ANSWER KEY

If an attendee gets stuck, or their Gemini instance writes code that doesn't work, use these exact blocks to fix their `services/` files.

### Ticket 1: Reverse Geocoding Utility (`services/geospatial.py`)
**Goal:** Fetch the City and Country from lat/lon coordinates.

```python
import requests
from config import logger
from services.vault import VaultService

class ReverseGeocode:
    @staticmethod
    def get_location_name(lat: float, lon: float) -> str:
        try:
            api_key = VaultService.get_maps_api_key()
            if not api_key:
                return "Unknown Location"

            url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data.get("status") == "OK" and data.get("results"):
                components = data["results"][0].get("address_components", [])
                city, country = "", ""

                for component in components:
                    types = component.get("types", [])
                    if "locality" in types:
                        city = component.get("long_name", "")
                    elif "country" in types:
                        country = component.get("long_name", "")

                if city and country:
                    return f"{city}, {country}"
                elif country:
                    return country
            
            return "Unknown Location"
        except Exception as e:
            logger.error(f"Reverse Geocode Error: {e}")
            return "Unknown Location"
```

### Ticket 2: Procedural Biome Generation (`services/ai_vision.py`)
**Goal:** The 2-stage generative pipeline (Gemini Architect + Imagen Painter).

```python
import base64
import json
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from config import GCPConfig, logger

class BiomeDesign(BaseModel):
    advisory: str = Field(description="A 1-sentence pilot advisory describing the transformation.")
    imagen_prompt: str = Field(description="A technical prompt for Imagen 3 to generate a thematic texture.")

class AIVisionService:
    @staticmethod
    def generate_biome_texture(city_name: str, user_prompt: str) -> dict:
        try:
            client = genai.Client(vertexai=True, project=GCPConfig.PROJECT_ID, location=GCPConfig.LOCATION)

            # STEP 1: The Biome Architect (Gemini 2.5 Flash)
            architect_prompt = f"""
            You are a Biome Architect. Design a procedural texture for {city_name}.
            Transform the terrain into: '{user_prompt}'.
            1. Generate a technical prompt for Imagen 3 describing a TOP-DOWN, high-resolution procedural map.
            2. Provide a short, 1-sentence pilot advisory.
            """

            gemini_response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=architect_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=BiomeDesign,
                    temperature=0.7
                )
            )
            
            design = BiomeDesign.model_validate_json(gemini_response.text)

            # STEP 2: The Texture Painter (Imagen 3)
            imagen_response = client.models.generate_images(
                model='imagen-3.0-generate-001',
                prompt=design.imagen_prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    output_mime_type="image/png"
                )
            )
            
            final_image_bytes = imagen_response.generated_images[0].image_bytes
            image_b64 = base64.b64encode(final_image_bytes).decode('utf-8')

            return {
                "advisory": design.advisory,
                "image_b64": image_b64
            }
        except Exception as e:
            logger.error(f"AI Vision Error: {e}")
            raise e
```

### Tickets 3 & 4: ADK Agents (`services/control_tower.py`)
**Goal:** The autonomous Control Tower Agent and the Copilot proxy.

```python
from google.genai import types
from google.adk import Agent, Runner
from google.adk.sessions import InMemorySessionService
from config import logger

def get_local_time(city_name: str) -> str:
    """Fetches the current local time for the specified city."""
    logger.info(f"Tool Execution: Fetching simulated time for {city_name}...")
    return "9:00 AM Local Time"

control_tower_agent = Agent(
    name="ControlTower",
    model="gemini-2.5-flash",
    instruction=(
        "You are the Global Control Tower AI. "
        "When a Copilot contacts you with their location, ALWAYS use the 'get_local_time' tool. "
        "Respond concisely with the local time and one interesting factoid about their city."
    ),
    tools=[get_local_time]
)

session_service = InMemorySessionService()
tower_runner = Runner(
    agent=control_tower_agent, 
    app_name="infinite_flight", 
    session_service=session_service, 
    auto_create_session=True
)

class CopilotAgent:
    @staticmethod
    def request_airspace_update(city_name: str) -> str:
        try:
            request_content = f"Control Tower, this is Flight 001 Copilot over {city_name}. Requesting time and local factoid."
            
            events = tower_runner.run(
                user_id="pilot_1",
                session_id="flight_001_session",
                new_message=types.Content(
                    role="user", 
                    parts=[types.Part.from_text(text=request_content)]
                )
            )

            final_text = ""
            for event in events:
                if getattr(event, 'error_message', None):
                    logger.error(f"ADK Event Error: {event.error_message}")
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            final_text += part.text

            final_text = final_text.strip()
            if not final_text:
                logger.warning(f"Copilot Agent: Received empty transmission. Using fallback.")
                return f"Captain, I'm getting static from the Control Tower over {city_name}. Standby."

            return final_text
        except Exception as e:
            logger.error(f"Copilot Agent Error: {e}")
            return f"Captain, unable to reach Control Tower. Clear conditions assumed for {city_name}."
```
