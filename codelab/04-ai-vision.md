# Module 4: Multimodal AI Vision (Visual RAG)

The core generative intelligence of the simulator resides within the `AIVisionService`. In this module, we implement a complex, two-stage **Visual Retrieval-Augmented Generation (RAG)** pipeline.

## The Two-Stage Terraforming Loop

1.  **Stage 1: The Analyst (Gemini 2.5 Flash):** Gemini analyzes the raw satellite image and the pilot's prompt to generate a technical image-to-image prompt and an immersive pilot advisory.
2.  **Stage 2: The Painter (Imagen 3):** Imagen 3 "repaints" the terrain based on the technical prompt, strictly adhering to the original street and structural topologies.

---

## Architecture: Visual RAG Sequence

![Architecture: AI Vision Pipeline](./assets/04_ai_vision.png)

*This sequence diagram illustrates our "Visual RAG" pipeline. Notice how the raw image bytes are analyzed by Gemini 2.5 Flash to understand geography before Imagen 3 applies the terraforming prompt.*

---

## Implementation: `AIVisionService`

**Action Marker 4.1:** Terminate the Flask server (CTRL+C). Open `services/ai_vision.py`, locate the `[CODELAB STEP 3B]` marker, and paste the following implementation. 

**Note:** This implementation uses the modern `google-genai` Unified SDK and Pydantic for strict JSON schema enforcement.

```python
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
```

**Action Marker 4.2:** Restart the Flask server (`uv run app.py`).

<br><span style="color:red; font-weight:bold;">📸 TAKE SCREENSHOT: Terraform a city (e.g., Cyberpunk) and capture the result! Save as `assets/03_cyberpunk_city.png`</span>
<br><span style="color:red; font-weight:bold;">📸 TAKE SCREENSHOT: Terraform 4 times in a row to trigger the memory limit. Capture the red "EVICTING OLD PATCH" toast notification! Save as `assets/04_memory_eviction.png`</span>

---

## 🛠 Troubleshooting AI Quotas

If you are using a new Google Cloud account, you might run into quota limitations:

*   **`429 Quota Exceeded`:** Vertex AI image generation limits are strict on fresh billing accounts. Wait 1-2 minutes and try terraforming again. 
*   **"API Not Enabled":** Verify that the **Vertex AI API** is enabled in your Google Cloud Console.
