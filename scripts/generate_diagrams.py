import os
import re
import vertexai
from vertexai.generative_models import GenerativeModel
import sys

# Add parent directory to path so we can import config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import GCPConfig

# Ensure Vertex AI is initialized
vertexai.init(project=GCPConfig.PROJECT_ID, location=GCPConfig.LOCATION)

DIAGRAMS = {
    "01_cloud_setup.svg": """graph LR
    CS[Cloud Shell / uv] -->|Auth via service-account-key.json| VAI[Vertex AI API]
    VAI -->|Gemini 2.5 Flash| IMG[Generated SVG Texture]
    IMG -->|Saved to| FILE[assets/texture.svg]""",
    
    "02_modular_architecture.svg": """graph TD
    Orch[app.py Orchestrator] --> Config[0. Config]
    Orch --> Vault[1. Secret Manager]
    Orch --> Geo[2. Earth Engine]
    Orch --> Vision[3. Vertex AI]
    Orch --> Audio[4. Cloud TTS]
    Orch --> State[5. Firestore]""",

    "03_geospatial_engine.svg": """graph LR
    Coord[Pilot Lat/Lon] --> EE[Earth Engine]
    EE -->|Satellite Query| S2[Sentinel-2 Data]
    S2 -->|Clipped to| B64[Raw Image Bytes]
    B64 -->|Grounded Input| Vision[Module 4: AI Vision]""",

    "04_ai_vision.svg": """sequenceDiagram
    participant App as app.py
    participant EE as Earth Engine
    participant G25 as Gemini 2.5 Flash
    participant I3 as Imagen 3

    App->>EE: Fetch Satellite PNG at Lat/Lon
    EE-->>App: Raw Image Bytes
    App->>G25: Analyze Image + "Mars Colony"
    G25-->>App: JSON {technical_prompt, advisory}
    App->>I3: edit_image(base_image, technical_prompt)
    I3-->>App: Terraformed Texture""",

    "05_immersive_audio.svg": """graph TD
    Text[AI Generated Text] --> TTS[Cloud TTS Engine]
    TTS -->|en-US-Studio-O| P[Pilot Audio]
    TTS -->|en-US-Journey-D| ATC[Control Tower Audio]
    P --> FE[Frontend Speaker]
    ATC --> FE""",

    "06_persistent_world.svg": """graph TD
    Button[Pilot Clicks 'WHERE AM I?'] --> Agent[Control Tower Agent<br>gemini-2.5-flash]
    
    subgraph Parallel ADK Loop
        Agent -->|Decides to use Tools| Decision{Orchestrator}
        Decision -->|get_telemetry| T1[Identify Landmark]
        Decision -->|scan_anomaly_tracker| T2[Scan Anomaly Tracker]
        
        T1 -.->|Vertex AI Vision| Decision
        T2 -.->|Cloud Firestore| Decision
    end
    
    Decision -->|Aggregated Data| Agent
    Agent -->|Immersive Text| TTS[Cloud Text-to-Speech]
    TTS -->|MP3 Audio| Pilot[Pilot Audio Player]"""
}

def generate_svgs():
    print("🧠 Loading Gemini 2.5 Flash...")
    model = GenerativeModel("gemini-2.5-flash")
    
    os.makedirs("assets", exist_ok=True)

    for filename, mermaid_code in DIAGRAMS.items():
        print(f"🎨 Generating SVG for {filename}...")
        
        prompt = f"""
        You are an expert technical diagram designer and SVG artist.
        I have a Mermaid diagram representing software architecture.
        I need you to convert this logic into a highly aesthetic, beautiful, self-contained SVG diagram.
        
        Style Requirements:
        - Dark mode (cyberpunk-ish or sleek modern cloud architecture).
        - Dark backgrounds (#0a0e17, #1f2833) with neon accents (cyan #66fcf1, magenta, or green).
        - Rounded nodes, glowing edges, and clean typography (sans-serif like Arial or Roboto).
        - The diagram must accurately represent the nodes and connections of the Mermaid code.
        - Ensure text is readable, correctly positioned, and doesn't overlap edges.
        - Add drop shadows or glow filters to the shapes.
        - Draw explicit arrows or sequence lines reflecting the Mermaid relationships.
        - Output width should be around 800px, height around 600px (or adjust as needed).
        
        Mermaid Code:
        {mermaid_code}
        
        Return ONLY the raw <svg>...</svg> code. Do not include markdown blocks, HTML, or explanations.
        """
        
        res = model.generate_content(prompt)
        svg_code = res.text.strip()
        
        # Robustly extract SVG from potential markdown
        if "```" in svg_code:
            match = re.search(r"<svg.*?</svg>", svg_code, re.IGNORECASE | re.DOTALL)
            if match:
                svg_code = match.group(0).strip()
            else:
                try:
                    svg_code = svg_code.split("```")[1].strip()
                    for prefix in ["xml", "svg", "html"]:
                        if svg_code.lower().startswith(prefix):
                            svg_code = svg_code[len(prefix):].strip()
                            break
                except IndexError:
                    pass
                        
        filepath = f"assets/{filename}"
        with open(filepath, "w") as f:
            f.write(svg_code)
            
        print(f"✅ Saved to {filepath}")

if __name__ == "__main__":
    generate_svgs()
