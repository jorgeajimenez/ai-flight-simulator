# Gemini Refactor Workspace

This file tracks the active refactoring status of the **Infinite Flight Simulator** to ensure alignment with the `REFACTOR_INSTRUCTIONS.md` and the `tickets.csv` task list.

## 🚀 Active Refactor: Service-Oriented TDD
We are currently deconstructing the `app.py` monolith into the **Essential 6 Google Cloud Stack**.

### 📋 Ticket Tracking
The current status of all tasks can be found in `tickets.csv`.

### 🛠 Refactor Workflow
1. **Plan & Track:** Before starting *any* new work, Gemini must add the task to `tickets.csv` with a clear description. We work strictly off this list.
2. **Gemini:** Identifies the next `TODO` ticket in `tickets.csv`.
3. **Gemini:** Writes the corresponding unit test in the `tests/` directory (Mocking all GCP calls).
4. **Gemini:** Implements the minimal logic in the `services/` or `config.py` module to pass the test.
5. **Gemini:** Updates `tickets.csv` to mark the task as `DONE`.
6. **User:** Manually verifies the simulator's integration (ensuring `app.py` still runs).

---

## 🧠 Engineering with AI (Core Philosophy)
- We are not just generating code; we are teaching attendees how to build with **Engineering in mind**.
- Attendees will use the **Gemini CLI** to generate the basic implementations of these services.
- The codelab will also teach them how to use the CLI to *improve* their code (e.g., adding error handling, strict typing, or edge-case testing).

---

## 🚦 Integration Points (`# AI_WIRING_POINT`)
As we refactor, we will inject these comments into `app.py` to facilitate the final assembly.

1. **Service 0 (Config):** `config.py` - PROJECT_ID, LOCATION, Logging.
2. **Service 1 (Vision):** `services/ai_vision.py` - Gemini + Imagen (or Gemini for textures).
3. **Service 2 (Geospatial):** `services/geospatial.py` - Earth Engine.
4. **Service 3 (Audio):** `services/audio_engine.py` - TTS.
5. **Service 4 (Persistence):** `services/state_sync.py` - Firestore.
6. **Service 5 (Vault):** `services/vault.py` - Secret Manager.
7. **Frontend Features:** The Radio, Procedural City Generation (`spawnProceduralCity`).

---

## 📝 Recent Memories
- Refactor is moving from Flask-monolith to Service-Oriented.
- Using `pytest` and `pytest-mock` for TDD.
- User handles integration testing after each modular step.
- **CRITICAL REQUIREMENT:** The codelab MUST be "Seamless". Build with re-buildability top of mind. Any manual configuration steps (like creating secrets in the UI) must be automated in setup scripts so attendees have a flawless, one-click start.
- Created `codelab/06-multiverse-state.md` to document the Firestore module built in Ticket 11/12.
- Added tasks 15-17 to handle "The Radio" (audio playback), Procedural City Generation, and using Gemini Flash for texture generation.
