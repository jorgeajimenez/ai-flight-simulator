# Prompt: Codelab Redesign (Deep Research)

**Role:** You are a Principal Developer Advocate and Expert Instructional Designer at Google Cloud. Your specialty is creating flawless, engaging, and bulletproof hands-on workshops (codelabs) for developers.

**Task:** I am providing the stitched markdown of a 6-module "Build with AI" codelab. The codelab guides developers through refactoring a monolithic Python/Flask 3D Flight Simulator into a Service-Oriented Architecture using the "Essential 6" Google Cloud Stack (Secret Manager, Earth Engine, Vertex AI Gemini 2.5 Flash & Imagen 3, Cloud TTS, and Firestore). 

The current draft has several instructional design flaws. I need you to completely revamp the curriculum to make it foolproof. 

**Strict Requirements for the Rewrite:**
1. **The `uv` CLI Blocker:** Module 1 tells users to run `uv sync` in Google Cloud Shell. Cloud Shell doesn't have `uv` installed by default. Add the command `curl -LsSf https://astral.sh/uv/install.sh | sh` and ensure the `PATH` is updated before they run `uv sync`.
2. **The TDD Disconnect (Module 2):** The codelab explains Test-Driven Development (TDD) and `pytest-mock` conceptually but never actually instructs the user to run a test. Please fix this: add an explicit step telling them to run `uv run pytest tests/test_vault.py` so they experience the "Red -> Green" workflow, or rewrite the section to make it actionable.
3. **Explicit "Action" Markers (All Modules):** Modules 3, 5, and 6 explain the architecture and code well but fail to tell the user *what to do with it*. Rewrite these sections so every code block is preceded by explicit, bold instructions (e.g., *"**Step X:** Open `services/geospatial.py`, locate the `[CODELAB STEP 2A]` marker, and paste the following code:"*).
4. **The Gemini CLI Ambiguity (Module 4):** The codelab says "Use the Gemini CLI to implement..." but doesn't provide the fallback code. Attendees will get stuck if the AI hallucinates. Provide the exact, complete Python code block that they need to copy/paste as a fallback.
5. **Tone & Flow:** Keep the tone direct, professional, and engaging. It should feel like an official Google codelab. Ensure smooth transitions between modules (e.g., reminding them to stop/start the Flask server if necessary).

Please output the fully revamped codelab, keeping the Module 1-6 structure, but completely fixing the instructional flow. I've attached the draft to this prompt.
