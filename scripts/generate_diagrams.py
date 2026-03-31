import os
import sys
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

# Add parent directory to path so we can import config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import GCPConfig

def main():
    print("🚀 Initializing Setup...")
    vertexai.init(project=GCPConfig.PROJECT_ID, location=GCPConfig.LOCATION)
    
    print("🧠 Loading Imagen 3 (imagen-3.0-generate-001)...")
    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
    
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "codelab", "assets")
    os.makedirs(out_dir, exist_ok=True)

    print(f"\n📁 Images will be saved to: {out_dir}/")

    # 1. THE ARCHITECTURE CHARTS
    mermaid_code_blocks = {
        "01_cloud_setup.png": """graph LR
    CS[Cloud Shell / uv] -->|Auth via service-account-key.json| VAI[Vertex AI API]
    VAI -->|Gemini 2.5 Flash| IMG[Generated SVG Texture]
    IMG -->|Saved to| FILE[assets/texture.svg]""",
        
        "02_modular_architecture.png": """graph TD
    Orch[app.py Orchestrator] --> Config[0. Config]
    Orch --> Vault[1. Secret Manager]
    Orch --> Geo[2. Earth Engine]
    Orch --> Vision[3. Vertex AI]
    Orch --> Audio[4. Cloud TTS]
    Orch --> State[5. Firestore]""",

        "03_geospatial_engine.png": """graph LR
    Coord[Pilot Lat/Lon] --> EE[Earth Engine]
    EE -->|Satellite Query| S2[Sentinel-2 Data]
    S2 -->|Clipped to| B64[Raw Image Bytes]
    B64 -->|Grounded Input| Vision[Module 4: AI Vision]""",

        "04_ai_vision.png": """sequenceDiagram
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

        "05_immersive_audio.png": """graph TD
    Text[AI Generated Text] --> TTS[Cloud TTS Engine]
    TTS -->|en-US-Studio-O| P[Pilot Audio]
    TTS -->|en-US-Journey-D| ATC[Control Tower Audio]
    P --> FE[Frontend Speaker]
    ATC --> FE""",

        "06_persistent_world.png": """graph TD
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

    # Extremely simple prompt to keep the image legible, focusing on the mermaid code directly.
    base_style = """
A clean, flat, highly legible software architecture diagram. Flight simulator aesthetic. Dark purple background, glowing cyan and neon green shapes. Very simple, large readable text. The exact nodes and structure are strictly defined by this Mermaid code:
"""

    dummy_prompts = {
        "dummy_web_preview.png": "A clean, minimalist 3D isometric illustration of a Google Cloud Shell 'Web Preview' button on a dark purple background. Show an eye icon and the text 'Preview on port 8080'. Glowing cyan neon accents.",
        "dummy_enable_apis.png": "A clean, minimalist 3D isometric illustration of a Google Cloud Console 'Enable APIs' screen on a dark purple background. Show a glowing blue 'ENABLE' button next to soft rounded text blocks.",
        "dummy_iam_roles.png": "A clean 3D isometric illustration of a Google Cloud IAM Roles assignment dropdown on a dark purple background. Show 'Vertex AI User' being assigned with glowing neon accents.",
        "dummy_secret_manager.png": "A clean 3D isometric illustration of a Google Cloud Secret Manager UI on a dark purple background. Show a glowing data table with a secret named 'GOOGLE_MAPS_API_KEY' and a green glowing checkmark.",
        "dummy_firestore.png": "A clean 3D isometric illustration of a Google Cloud Firestore setup screen on a dark purple background. Show a dialog box selecting 'Native Mode' and a glowing 'Create Database' button."
    }

    print("\n--- Interactive Generation Menu: Architecture Diagrams (Imagen 3) ---")
    
    # Process Diagrams via Imagen 3 directly
    for filename, mermaid in mermaid_code_blocks.items():
        full_prompt = base_style + f"\n```mermaid\n{mermaid}\n```"
        
        ans = input(f"\n▶️  Generate '{filename}'? [Press Enter to start, 's' to skip, 'q' to quit]: ").strip().lower()
        if ans == 'q':
            print("Exiting.")
            return
        if ans == 's':
            continue
            
        print(f"🎨 Generating {filename} with Imagen 3...")
        try:
            response = model.generate_images(
                prompt=full_prompt,
                number_of_images=1
            )
            if response.images:
                generated_image = response.images[0]
                filepath = os.path.join(out_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(generated_image._image_bytes)
                print(f"  ✅ Saved aesthetic PNG to {filepath}")
            else:
                print(f"  ❌ No image returned for {filename}")
        except Exception as e:
            print(f"  ❌ Failed to generate {filename}: {e}")

    print("\n--- Interactive Generation Menu: UI Placeholders (Imagen 3) ---")
    
    # Process Dummy UIs
    for filename, prompt_text in dummy_prompts.items():
        ans = input(f"\n▶️  Generate '{filename}'? [Press Enter to start, 's' to skip, 'q' to quit]: ").strip().lower()
        if ans == 'q':
            print("Exiting.")
            return
        if ans == 's':
            continue
            
        print(f"🎨 Generating {filename} with Imagen 3...")
        try:
            response = model.generate_images(
                prompt=prompt_text,
                number_of_images=1
            )
            if response.images:
                generated_image = response.images[0]
                filepath = os.path.join(out_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(generated_image._image_bytes)
                print(f"  ✅ Saved aesthetic PNG to {filepath}")
            else:
                print(f"  ❌ No image returned for {filename}")
        except Exception as e:
            print(f"  ❌ Failed to generate {filename}: {e}")

if __name__ == "__main__":
    main()
