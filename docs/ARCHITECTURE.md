# V2 Architecture: Procedural Biomes & ADK Agents

The V2 Infinite Flight Simulator replaces monolithic static scripts with a modern, AI-first **Service-Oriented Architecture (SOA)**.

## 1. High-Level Modular Architecture

```mermaid
graph TD
    App[app.py Orchestrator] --> Config[config.py / Logging]
    App --> Vault[VaultService: Secret Manager]
    App --> Geo[GeospatialService: Reverse Geocoding]
    App --> Vision[AIVisionService: Procedural Biomes]
    App --> Audio[4. Cloud TTS]
    App --> Agents[5. ADK Control Tower]
    ```

    ## 2. The Procedural Terraforming Flow (Ticket 2)

    Instead of complex image-to-image alignment, V2 utilizes a Generative Pipeline to create procedural textures based on the pilot's coordinates.

    ```mermaid
    sequenceDiagram
    participant FE as Frontend (Cesium)
    participant App as app.py
    participant Geo as ReverseGeocode
    participant G25 as Gemini 2.5 Flash
    participant I3 as Imagen 3
    participant FS as Firestore (Event Log)

    FE->>App: POST /terraform {lat, lon, prompt}
    App->>Geo: get_location_name(lat, lon)
    Geo-->>App: "City, Country"
    App->>G25: Architect Prompt ("City", "prompt")
    G25-->>App: JSON {technical_imagen_prompt, advisory}
    App->>I3: Generate Image (technical_imagen_prompt)
    I3-->>App: Raw Image Bytes
    App->>FS: log_terraform_event(lat, lon, Image, Prompt)
    App-->>FE: {image_b64, audio_advisory, texture_url}
    ```

    ## 3. The Agent-to-Agent (A2A) Workflow (Tickets 3 & 4)

We use the Google Agent Development Kit (ADK) to build an autonomous Control Tower that uses tools.

```mermaid
sequenceDiagram
    participant FE as Frontend
    participant Copilot as CopilotAgent (Python)
    participant Tower as ControlTowerAgent (ADK Runner)
    participant Tool as get_local_time (Python Tool)
    
    FE->>Copilot: Click 'WHERE AM I?'
    Copilot->>Tower: "Flight 001 over {City}, requesting time."
    
    rect rgb(30, 30, 50)
        Note over Tower, Tool: Google ADK Autonomous Loop
        Tower->>Tower: LLM Reasoning: "I need local time."
        Tower->>Tool: execute(City)
        Tool-->>Tower: "9:00 AM Local Time"
        Tower->>Tower: Synthesize final briefing
    end
    
    Tower-->>Copilot: Final Text Briefing
    Copilot-->>FE: Briefing Audio (Cloud TTS)
```
