import os
import sys
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

# Add parent directory to path so we can import config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import GCPConfig

def main():
    print("🚀 Initializing Vertex AI...")
    vertexai.init(project=GCPConfig.PROJECT_ID, location=GCPConfig.LOCATION)
    
    print("🧠 Loading Imagen 3 (imagen-3.0-generate-001)...")
    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
    
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "codelab", "assets")
    os.makedirs(out_dir, exist_ok=True)

    print(f"\n📁 Images will be saved to: {out_dir}/")

    # Simplified, minimalist prompts with VERY little text to prevent rendering issues.
    # Flight simulator HUD/Cyberpunk theme.
    diagram_prompts = {
        "01_cloud_setup.png": "Minimalist futuristic flight HUD diagram. Three glowing digital icons: a terminal, a brain, and a file. Connected by neon cyan data streams. Minimal text. Dark mode.",
        
        "02_modular_architecture.png": "Futuristic flight radar screen. Central core icon with 6 surrounding nodes connected by glowing targeting lines. High-tech interface. Minimal text. Neon green.",

        "03_geospatial_engine.png": "Aero-navigation HUD. A 3D globe icon with a data flow pointing to a 'Vision' node. Minimalist orange glowing lines. High-tech. Minimal text.",

        "04_ai_vision.png": "Flight simulator HUD sequence. A horizontal flow of 4 technical icons connected by purple data streaks. Dark technical blueprint style. Minimal text.",

        "05_immersive_audio.png": "Futuristic audio waveform interface. A speaker icon branching into a headset and a radar tower. Neon yellow glowing soundwaves. Minimal text.",

        "06_persistent_world.png": "Tactical flight map. A central AI core node connected to two scanning sub-nodes. Glowing cyan and pink tactical elements. Complex technical blueprint. Minimal text."
    }

    dummy_prompts = {
        "dummy_web_preview.png": "Minimalist dark mode flight HUD button icon: an eye symbol with text '8080'. Cyan neon.",
        "dummy_enable_apis.png": "Minimalist dark mode UI mockup: a glowing blue 'ENABLE' button. High-tech interface.",
        "dummy_iam_roles.png": "Minimalist flight HUD radar screen showing a user role icon. Neon green accents.",
        "dummy_secret_manager.png": "Minimalist dark mode UI mockup: a secret key icon with a green checkmark. Technical UI.",
        "dummy_firestore.png": "Minimalist dark mode UI mockup: a database icon with a 'Create' button. Glowing blue."
    }

    all_prompts = {**diagram_prompts, **dummy_prompts}

    print("\n--- Interactive Generation Menu ---")
    for filename, prompt_text in all_prompts.items():
        ans = input(f"\n▶️  Generate '{filename}'? [Press Enter to start, 's' to skip, 'q' to quit]: ").strip().lower()
        if ans == 'q':
            print("Exiting.")
            return
        if ans == 's':
            continue
            
        print(f"🎨 Processing {filename} with Imagen 3...")
        
        try:
            # Removed aspect_ratio to fix compatibility error. 
            # Simplified arguments for maximum compatibility with current SDK version.
            response = model.generate_images(
                prompt=prompt_text,
                number_of_images=1
            )
            
            if response.images:
                generated_image = response.images[0]
                filepath = os.path.join(out_dir, filename)
                
                with open(filepath, "wb") as f:
                    f.write(generated_image._image_bytes)
                    
                print(f"  ✅ Saved to {filepath}")
            else:
                print(f"  ❌ No image returned for {filename}")
                
        except Exception as e:
            print(f"  ❌ Failed to generate {filename}: {e}")

if __name__ == "__main__":
    main()
