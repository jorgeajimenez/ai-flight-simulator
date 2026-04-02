import requests
import base64
import json
import os

mermaid_code_blocks = {
    "01_cloud_setup.png": """graph LR
CS[Cloud Shell / uv] -->|Auth via service-account-key.json| VAI[Vertex AI API]
VAI -->|Gemini 2.5 Flash| IMG[Generated Texture]
IMG -->|Saved to| FILE[assets/texture.png]""",
    
    "02_modular_architecture.png": """graph TD
App[app.py Orchestrator] --> Config[0. Config]
App --> Vault[1. Secret Manager]
App --> Geo[2. Reverse Geocoding]
App --> Vision[3. Procedural Biomes]
App --> Audio[4. Cloud TTS]
App --> State[5. Firestore Ledger]
App --> Agents[6. ADK Control Tower]""",

    "03_telemetry_geocoding.png": """graph LR
Coord[Pilot Lat/Lon] --> Geo[ReverseGeocode Utility]
Geo -->|Google Maps API| API[Geocoding API]
API -->> Geo: JSON Data
Geo -->> Output[City, Country Name]""",

    "04_generative_biomes.png": """sequenceDiagram
participant App
participant G25 as Gemini (Architect)
participant I3 as Imagen 3 (Painter)

App->>G25: City Name + User Prompt
G25-->>App: JSON {technical_prompt, advisory}
App->>I3: Generate Image(technical_prompt)
I3-->>App: Raw Image Bytes""",

    "05_immersive_audio.png": """graph TD
Text[AI Generated Advisory] --> TTS[Cloud TTS Engine]
TTS -->|en-US-Journey-D| ATC[Audio Bytes]
ATC --> FE[Frontend Speaker]""",

    "06_collaborative_agents.png": """sequenceDiagram
participant FE as Frontend
participant Copilot as Copilot Agent
participant Tower as ADK Control Tower
participant Tool as get_local_time Tool

FE->>Copilot: Request Airspace Update
Copilot->>Tower: "Flight 001 over City, requesting time."
Tower->>Tool: execute(City Name)
Tool-->>Tower: "9:00 AM Local Time"
Tower-->>Copilot: Synthesized Briefing
Copilot-->>FE: Final Audio Briefing"""
}

out_dir = os.path.join("codelab", "assets")
os.makedirs(out_dir, exist_ok=True)

for filename, code in mermaid_code_blocks.items():
    # Mermaid ink requires base64 encoded string
    # We create a config to make the diagram look good (dark mode)
    state = {
        "code": code,
        "mermaid": {
            "theme": "dark"
        }
    }
    json_str = json.dumps(state)
    b64_str = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    
    url = f"https://mermaid.ink/img/{b64_str}?type=png"
    
    print(f"Fetching {filename}...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(out_dir, filename), 'wb') as f:
                f.write(response.content)
            print(f"Saved {filename}")
        else:
            print(f"Failed {filename}: {response.status_code}")
    except Exception as e:
        print(f"Error {filename}: {e}")
