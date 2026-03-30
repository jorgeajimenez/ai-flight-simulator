import json
import base64
import re
from io import BytesIO
from typing import Dict
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from vertexai.preview.vision_models import Image as VertexImage, ImageGenerationModel
from config import GCPConfig, logger

# Initialize Vertex AI SDK
vertexai.init(project=GCPConfig.PROJECT_ID, location=GCPConfig.LOCATION)

class AIVisionService:
    """
    Multimodal Intelligence powered by Vertex AI.
    Handles terrain analysis with Gemini 1.5 Flash and terraforming with Imagen 3.
    """

    @staticmethod
    def generate_texture(prompt: str) -> str:
        """
        Uses Gemini 2.0 Flash to generate high-quality SVG texture code for 3D objects.
        Returns a base64 encoded SVG string for the frontend.
        """
        try:
            gemini_model = GenerativeModel("gemini-2.5-flash")
            svg_prompt = f"""
            Generate a minimal, tiled SVG texture for a 3D building. Theme: '{prompt}'.
            Focus on neon windows, metallic surfaces, or futuristic patterns.
            Return ONLY the raw <svg>...</svg> code without any markdown or formatting.
            """
            
            logger.info(f"AI Vision: Generating dynamic SVG texture for '{prompt}'...")
            res = gemini_model.generate_content(svg_prompt)
            
            svg_code = res.text.strip()
            # AI_WIRING_POINT: Handle potential markdown wrappers from Gemini
            # Robustly handle markdown wrappers to prevent malformed SVGs
            if "```" in svg_code:
                match = re.search(r"<svg.*?</svg>", svg_code, re.IGNORECASE | re.DOTALL)
                if match:
                    svg_code = match.group(0).strip()
                else:
                    # Fallback string stripping
                    svg_code = svg_code.split("```")[1].strip()
                    for prefix in ["xml", "svg", "html"]:
                        if svg_code.lower().startswith(prefix):
                            svg_code = svg_code[len(prefix):].strip()
                            break
                
            return base64.b64encode(svg_code.encode('utf-8')).decode('utf-8')
        except Exception as e:
            logger.error(f"AI Vision Texture Error: {e}")
            return ""

    @staticmethod
    def describe_location(lat: float, lon: float) -> str:
        """
        Uses Gemini to generate a short pilot advisory about their current global position.
        """
        try:
            gemini_model = GenerativeModel("gemini-2.5-flash")
            prompt = f"""
            You are an AI flight computer in a flight simulator. 
            The pilot is flying at exactly Latitude {lat}, Longitude {lon}.
            In exactly one short sentence (max 20 words), tell the pilot what real-world region, city, or landmark they are flying over. Be immersive.
            """
            logger.info(f"AI Vision: Identifying location at {lat}, {lon}...")
            res = gemini_model.generate_content(prompt)
            return res.text.strip()
        except Exception as e:
            logger.error(f"AI Vision Location Error: {e}")
            return "Sensors offline. Unable to determine current location."

    @staticmethod
    def analyze_and_terraform(image_bytes: bytes, user_prompt: str) -> Dict[str, str]:
        """
        The 2-Stage Terraforming Pipeline:
        1. Gemini analyzes satellite image and engineers a technical prompt.
        2. Imagen 3 performs image-to-image transformation using the engineered prompt.
        """
        try:
            # Stage 1: Gemini Strategic Analysis
            gemini_model = GenerativeModel("gemini-2.5-flash")
            terrain_image = Part.from_data(data=image_bytes, mime_type="image/png")
            
            gemini_prompt = f"""
            Analyze this satellite image. The user wants to terraform this into: '{user_prompt}'.
            1. Create a narrative 'Flight Advisory' for the pilot (max 30 words).
            2. Generate a highly detailed Imagen prompt starting with 'A photorealistic high-resolution aerial view of'.
            Return JSON exactly matching this structure: {{"advisory": "string", "imagen_prompt": "string"}}
            """
            
            logger.info(f"AI Vision: Analyzing terrain for '{user_prompt}'...")
            gemini_res = gemini_model.generate_content(
                [terrain_image, gemini_prompt],
                generation_config={"response_mime_type": "application/json"}
            )
            
            ai_plan = json.loads(gemini_res.text.strip())
            logger.info(f"AI Vision: Pilot Advisory: {ai_plan.get('advisory')}")

            # Stage 2: Imagen 3 Terraforming
            imagen_model = ImageGenerationModel.from_pretrained("imagegeneration@006")
            base_image = VertexImage(image_bytes=image_bytes)
            
            logger.info(f"AI Vision: Terraforming with Imagen 3...")
            generated_images = imagen_model.edit_image(
                base_image=base_image, 
                prompt=ai_plan['imagen_prompt']
            )
            
            # Save output to buffer and encode as Base64
            output_buffer = BytesIO()
            generated_images[0].save(output_buffer, include_generation_parameters=False)
            generated_img_b64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
            
            return {
                "image_b64": generated_img_b64,
                "advisory": ai_plan.get("advisory", "")
            }
        except Exception as e:
            logger.error(f"AI Vision Terraforming Error: {e}")
            raise e
