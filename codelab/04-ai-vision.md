# Module 4: Multimodal AI Vision (Grounded Terraforming)

This is the most advanced part of the simulator's brain. In this module, we will build a **Visual RAG** pipeline. We don't just generate a random image; we use **Google Earth Engine** data to ground our generation in the real world.

The `AIVisionService` acts as our multimodal intelligence hub, providing two key functions:
1.  `describe_location`: Generating short pilot advisories about their current global position.
2.  `analyze_and_terraform`: A complex 2-stage generative pipeline for transforming the terrain.

## The 2-Stage Terraforming Loop

1.  **Stage 1: The Analyst (Gemini 2.5 Flash):** We send the raw satellite bytes to Gemini along with the pilot's prompt. Gemini analyzes the terrain and engineers a *technical* prompt for the image generator, returning a structured JSON response containing the prompt and a pilot advisory.
2.  **Stage 2: The Painter (Imagen 3):** We pass the engineered technical prompt and the *original* image to Imagen 3 (`imagegeneration@006`). Using image-to-image translation, Imagen "repaints" the world while keeping every street and building footprint exactly where they are in reality.

---

## Architecture: Visual RAG Sequence
This diagram shows how we move from a 1D text prompt to a 2D geographically grounded texture.

![Architecture: AI Vision Pipeline](../assets/04_ai_vision.svg)

---

## Implementation: `AIVisionService`

Open `services/ai_vision.py` and find **[CODELAB STEP 3B]**. You will use the Gemini CLI to implement the following within `analyze_and_terraform`:

```python
# [CODELAB STEP 3B]
# 1. Stage 1: Initialize gemini-2.5-flash
# 2. Create a 'Part' from the satellite bytes
# 3. Request strict JSON output containing 'advisory' and 'imagen_prompt'
# 4. Stage 2: Initialize imagegeneration@006
# 5. Call edit_image with the base_image and engineered prompt
```