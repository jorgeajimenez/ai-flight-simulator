# GDG Codelab Cleanup & Polish Plan

**Event Date:** April 2, 2026
**Goal:** Transform the working prototype into a high-quality, professional Google Codelab experience. The codebase must be robust, readable, and structured so attendees can successfully complete the workshop without getting lost.

## Phase 1: Repository & Artifact Cleanup
Remove cruft and ensure the project looks professional upon cloning.
- [ ] **Delete unwanted files:** Remove `service-account-key.json.bak` and any other leftover artifacts.
- [ ] **Clean `.gitignore`:** Ensure `.env`, `.venv`, `__pycache__`, `.pytest_cache`, and `*.json.bak` are properly ignored.
- [ ] **Dependency Management:** Verify `pyproject.toml`, `uv.lock`, and `requirements.txt` are synced and clearly documented since the codelab uses `uv` for Python environments.

## Phase 2: Code Quality & Formatting (The "Google" Standard)
Attendees will be reading this code. It needs to be extremely clean.
- [ ] **Python Formatting:** Run `ruff` or a formatter over `app.py`, `config.py`, and all files in `services/` and `tests/`.
- [ ] **Docstrings:** Ensure every class and method in `services/` has a clear, beginner-friendly docstring explaining *what* it does and *why* it's needed for the 3D simulator.
- [ ] **Frontend Polish:** `index.html` is a massive 4,000+ line monolith. While we might not have time to split it into React components today, we must run a formatter (like Prettier) over it and ensure the inline CSS/JS is indented correctly and sectioned with clear ASCII headers (e.g., `// --- AUDIO ENGINE ---`).

## Phase 3: Starter vs. Solution State (CRITICAL)
Currently, the codebase contains the **completed** logic for all services. If attendees clone this, the workshop is already finished.
- [ ] **Save the Solution:** Commit the current working state to a `solution` branch (or a `solution/` directory).
- [ ] **Create the Starter Template:** On the `main` branch, strip out the actual API calls inside `services/ai_vision.py`, `services/geospatial.py`, etc.
- [ ] **Add Codelab Markers:** Replace the stripped code with clear `TODO: [CODELAB STEP X] Implement Gemini API call here` comments so attendees know exactly where to paste the code they generate using the Gemini CLI.

## Phase 4: Documentation & Guides
If the instructions fail, the attendees fail.
- [ ] **Review `README.md`:** Ensure it explicitly points attendees to the starting point.
- [ ] **Review `CLOUD_SETUP.md` & `INSTALL_GUIDE.md`:** Verify the setup scripts (`setup_gcp.sh`/`.ps1`) perfectly match the required APIs (Earth Engine, Vertex AI, Secret Manager, TTS, Firestore). Ensure instructions mention `uv run` where appropriate.
- [ ] **Review `codelab/*.md`:** Ensure the markdown guides match the newly refactored `services/` architecture. For example, Step 4 should specifically mention editing `services/ai_vision.py`, not `app.py`.

## Next Steps
Once approved, I will execute these phases sequentially. I recommend we start with Phase 1 & 2 immediately to lock in the code quality, then branch off for Phase 3.
