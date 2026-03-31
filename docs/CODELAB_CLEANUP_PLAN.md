# 🧹 GDG Codelab Cleanup & Polish Plan

**Event Date:** April 2, 2026
**Goal:** Transform the current prototype into the "Starter" repo that attendees will clone. We will strip the working logic and replace it with clear instructions, while keeping the "Solution" safely in its own branch.

## 🚀 Phase 1: Terminology & Lore Alignment
Ensure the project uses consistent, easy-to-understand language.
- [ ] **Rename "Multiverse":** Replace all references to "Multiverse" with **"Persistent World"** (for the database) or **"Anomaly Tracker"** (for the ATC Radar).
- [ ] **Update Codelab Files:** Search and replace "Multiverse" in `codelab/*.md` to match the new lore.

## 📦 Phase 2: Repository Cleanup (CLI/SVGs)
- [ ] **Static Assets:** Ensure `assets/texture.svg` is the primary demo asset, and remove any leftover PNG textures that are no longer used.
- [ ] **Dependency Audit:** Verify `uv sync` correctly installs all dependencies for the offline CLI scripts (`generate_texture.py`).
- [ ] **Remove Cruft:** Delete `fix_*.js`, `fix_*.py`, `test_sm.py`, and any other temporary scripts used during the refactor.

## 💎 Phase 3: The "Google" Code Standard
- [ ] **Formatting:** Run `ruff format` on all `.py` files and `Prettier` (if available) on `index.html`.
- [ ] **Docstrings:** Add high-quality docstrings to every service in `services/`.
- [ ] **Frontend Markers:** Break up the 4,000+ lines of `index.html` with clear ASCII section headers (e.g., `// === GEOSPATIAL ENGINE ===`).

## ✂️ Phase 4: Starter Template Creation (CRITICAL)
This is where we "break" the code so the attendees can fix it.
- [ ] **Strip Services:** In `services/`, remove the actual SDK calls (Vertex AI, Earth Engine, Secret Manager, TTS, Firestore) but keep the method signatures and logging.
- [ ] **Inject TODOs:** Add clear comments like `# TODO: [CODELAB STEP X] - Use Gemini CLI to fetch the API Key from Secret Manager here`.
- [ ] **Stub the CLI:** Empty the core logic of `generate_texture.py` so the "Icebreaker" module requires them to use Gemini CLI to write the first script.

## 📝 Phase 5: Documentation Final Review
- [ ] **Update README.md:** Explicitly state: "You are currently on the STARTER branch. If you get stuck, the full code is on the SOLUTION branch."
- [ ] **Verify Guides:** Double-check `DEPLOY_TEST_GUIDE.md` and `INSTALL_GUIDE.md` for any remaining "Multiverse" references.

---
### Status Summary
1. **Solution State:** ✅ SAVED & PUSHED to `solution` branch.
2. **Current Branch:** `main` (Ready for stripping).
