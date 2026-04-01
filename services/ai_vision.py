import base64
import json
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from config import GCPConfig

# Define the deterministic JSON structure required from Gemini 2.5 Flash
class VisionAnalysis(BaseModel):
    advisory: str = Field(description="A short pilot briefing describing the terrain transformation.")
    imagen_prompt: str = Field(description="A detailed technical prompt optimized for Imagen 3.")

class AIVisionService:

    @staticmethod
    def analyze_and_terraform(base_image_bytes: bytes, user_prompt: str) -> dict:
        # Initialize the unified Vertex AI GenAI client
        client = genai.Client(
            vertexai=True,
            project=GCPConfig.PROJECT_ID,
            location=GCPConfig.LOCATION
        )

        # STAGE 1: The Analyst (Gemini 2.5 Flash)
        image_part = types.Part.from_bytes(data=base_image_bytes, mime_type="image/png")
        
        analysis_prompt = (
            f"Analyze this satellite image. The pilot wants to terraform this area into: '{user_prompt}'. "
            "Generate a technical prompt for an image generator that maintains the current road layout. "
            "Also provide a 1-sentence pilot advisory describing the anomaly."
        )

        # Execute generation with strict Pydantic JSON schema enforcement
        gemini_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[analysis_prompt, image_part],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=VisionAnalysis,
                temperature=0.4
            )
        )
        
        analysis_data = VisionAnalysis.model_validate_json(gemini_response.text)

        # STAGE 2: The Painter (Imagen 3)
        imagen_response = client.models.generate_images(
            model='imagen-3.0-generate-001',
            prompt=analysis_data.imagen_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                include_rai_reason=True,
                output_mime_type="image/jpeg"
            )
        )
        
        final_image_bytes = imagen_response.generated_images[0].image_bytes
        image_b64 = base64.b64encode(final_image_bytes).decode('utf-8')

        return {
            "advisory": analysis_data.advisory,
            "image_b64": image_b64
        }
