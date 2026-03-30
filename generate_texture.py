import argparse
import base64
import re
import vertexai
from vertexai.generative_models import GenerativeModel
from config import GCPConfig

def generate_building_texture(prompt: str):
    """
    Icebreaker Script: Generate a custom building texture using Gemini 2.5 Flash.
    """
    print(f"🚀 Initializing Vertex AI in project: {GCPConfig.PROJECT_ID}...")
    vertexai.init(project=GCPConfig.PROJECT_ID, location=GCPConfig.LOCATION)

    print("🧠 Loading Gemini 2.5 Flash...")
    gemini_model = GenerativeModel("gemini-2.5-flash")
    
    svg_prompt = f"""
    Generate a minimal, tiled SVG texture for a 3D building. Theme: '{prompt}'.
    Focus on neon windows, metallic surfaces, or futuristic patterns.
    Return ONLY the raw <svg>...</svg> code without any markdown or formatting.
    """
    
    print(f"🎨 Generating texture: '{prompt}'")
    res = gemini_model.generate_content(svg_prompt)
    svg_code = res.text.strip()
    
    # Robustly extract SVG from potential markdown
    if "```" in svg_code:
        match = re.search(r"<svg.*?</svg>", svg_code, re.IGNORECASE | re.DOTALL)
        if match:
            svg_code = match.group(0).strip()
        else:
            svg_code = svg_code.split("```")[1].strip()
            for prefix in ["xml", "svg", "html"]:
                if svg_code.lower().startswith(prefix):
                    svg_code = svg_code[len(prefix):].strip()
                    break

    output_path = "assets/texture.svg"
    with open(output_path, "w") as f:
        f.write(svg_code)
    
    print(f"✅ Success! Your custom texture has been saved to '{output_path}'.")
    print("Refresh your flight simulator browser to see your custom buildings!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a custom 3D building texture using Gemini 2.5 Flash.")
    parser.add_argument(
        "prompt", 
        type=str, 
        nargs="?", 
        default="glowing neon cyberpunk, rain, high tech", 
        help="Description of your building windows (e.g., 'rusty mars colony' or 'glowing neon cyberpunk')"
    )
    args = parser.parse_args()

    generate_building_texture(args.prompt)
