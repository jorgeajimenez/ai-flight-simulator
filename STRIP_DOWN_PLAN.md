# Creating the `main` (Codelab) Branch: The "Strip-Down" Plan

This document outlines the exact steps required to transition the fully functional `solution-slim` branch into the `main` branch that attendees will clone to begin the workshop.

**CRITICAL RULE:** Do NOT delete files entirely. Attendees rely on the file structure existing so they can use Gemini CLI to implement the missing logic. We only clear the *bodies* of specific functions and replace them with `# TODO` markers.

## 1. `tickets_v2.csv`
- Change all `DONE` statuses back to `TODO`.

## 2. `services/geospatial.py`
- Leave the `import` statements and the `class ReverseGeocode:` definition.
- **Strip:** The body of `def get_location_name(lat: float, lon: float) -> str:`.
- **Replace with:**
  ```python
  # TODO: [TICKET 1] Implement Reverse Geocoding via Google Maps API
  return "Unknown Location"
  ```

## 3. `services/ai_vision.py`
- Leave the `import` statements, the `BiomeDesign` Pydantic class, and the `class AIVisionService:` definition.
- **Strip:** The body of `def generate_biome_texture(city_name: str, user_prompt: str) -> dict:`.
- **Replace with:**
  ```python
  # TODO: [TICKET 2] Implement Procedural Biome Generation via Gemini & Imagen 3
  return {
      "advisory": "This is a placeholder advisory.",
      "image_b64": "" # Base64 encoded string of the image
  }
  ```

## 4. `services/control_tower.py`
- Leave the `import` statements.
- **Strip:** The `get_local_time` function, the `control_tower_agent` initialization, the `tower_runner` initialization, and the entire `CopilotAgent` class.
- **Replace with:**
  ```python
  # TODO: [TICKET 3] Implement the ADK Control Tower Agent and Tool

  class CopilotAgent:
      @staticmethod
      def request_airspace_update(city_name: str) -> str:
          # TODO: [TICKET 4] Implement the Copilot Agent to invoke the ADK Runner
          return f"Captain, we are currently holding pattern over {city_name}."
  ```

## 5. `app.py`
- Leave the imports, the standard Flask setup (`@app.route("/")`), and the `if __name__ == "__main__":` block.
- **Strip:** The entire `@app.route("/locate")` and `@app.route("/terraform")` routes.
- **Replace with:**
  *(Attendees are instructed in Module 2 to copy/paste the full routes from the codelab markdown, so these routes should simply be missing, or left as empty stubs with a comment).*
  ```python
  # TODO: Paste the /locate route here (See Module 2)

  # TODO: Paste the /terraform route here (See Module 2)
  ```

## 6. Cleanup Assets
- Ensure `assets/texture.svg` does not exist in the repo (so they must run the `scripts/generate_texture.py` icebreaker to generate it).

**Verification:** The `codelab/*.md` files and `DRY_RUN_GUIDE.md` have already been fully synchronized with the `solution-slim` logic, including all the recent ADK error fallbacks. They require zero modifications during this strip-down phase.