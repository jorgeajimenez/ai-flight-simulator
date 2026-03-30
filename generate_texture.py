import argparse
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from config import GCPConfig

def generate_building_texture(prompt: str):
    """
    Icebreaker Script: Generate a custom building texture using Imagen 3.
    """
    print(f"🚀 Initializing Vertex AI in project: {GCPConfig.PROJECT_ID}...")
    vertexai.init(project=GCPConfig.PROJECT_ID, location=GCPConfig.LOCATION)

    print("🧠 Loading Imagen 3 Model (imagegeneration@006)...")
    model = ImageGenerationModel.from_pretrained("imagegeneration@006")

    # Enhance the prompt to make it a good building texture
    enhanced_prompt = f"A seamless, flat, high contrast 2D texture of skyscraper windows. Theme: {prompt}."
    print(f"🎨 Generating texture: '{enhanced_prompt}'")

    # Generate the image
    images = model.generate_images(
        prompt=enhanced_prompt,
        number_of_images=1,
        aspect_ratio="1:1" # Perfect square for 3D tiling
    )

    # Save over the default texture
    output_path = "assets/cyberpunk_texture.png"
    images[0].save(output_path, include_generation_parameters=False)
    
    print(f"✅ Success! Your custom texture has been saved to '{output_path}'.")
    print("Refresh your flight simulator browser to see your custom buildings!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a custom 3D building texture using Imagen 3.")
    parser.add_argument(
        "prompt", 
        type=str, 
        nargs="?", 
        default="glowing neon cyberpunk, rain, high tech", 
        help="Description of your building windows (e.g., 'rusty mars colony' or 'glowing neon cyberpunk')"
    )
    args = parser.parse_args()

    generate_building_texture(args.prompt)
