# Publication Gaps: Infinite Flight Simulator

This document outlines the missing components and required refinements to prepare the **Infinite Flight Simulator** repository for official Google/Open-Source publication.

## 1. Mandatory Open-Source Boilerplate
Google-published projects must include standard legal and contribution files:
- [ ] **LICENSE:** Add an **Apache 2.0 License** file to the root.
- [ ] **CONTRIBUTING.md:** Define how external developers can contribute to the project.
- [ ] **CODE_OF_CONDUCT.md:** Include the standard Google Open Source Code of Conduct.
- [ ] **SECURITY.md:** Provide instructions on how to report security vulnerabilities.

## 2. Documentation & Codelab Alignment (CRITICAL)
There is currently a discrepancy between the "V2 Architecture" (which purges Earth Engine) and the existing documentation.
- [ ] **Remove Earth Engine References:** 
    - Update `codelab/03-telemetry-geocoding.md` (currently references Earth Engine registration).
    - Update `GEMINI.md` to remove `earthengine-api` from the tech stack.
    - Update `README.md` and any HTML scratchpads (`my_codelab.html`) to remove registration steps for Earth Engine.
- [ ] **Synchronize Ticket Files:** Resolve the difference between `tickets_v2.csv` (4 tickets) and `docs/tickets.csv` (17 tickets). Use a single source of truth.
- [ ] **Update `app.py` Instructions:** `GEMINI.md` states `app.py` is "locked," but it contains `TODO` markers. The instructions should clarify if attendees are expected to modify this file or if it's pre-populated in the solution branch.
- [ ] **Architecture Diagrams:** Embed the architecture diagrams directly into the `README.md` for better visibility on GitHub.

## 3. Repository Cleanup
The repository contains several "scratch" or temporary files that should be removed before publication:
- [ ] **Remove Junk Files:** `cat_placeholder.jpeg`, `lol.png`.
- [ ] **Remove Debug Scripts:** `debug_adk*.py`.
- [ ] **Remove Rendered HTML:** `codelab.html`, `my_codelab.html` (the source should be the markdown files in `/codelab`).
- [ ] **Remove Internal Scripts:** `fix_mermaid.py`, `render_mermaid.py` (unless intended for the end-user).

## 4. Setup Script Enhancements
- [ ] **GCP API Verification:** Verify if `geocoding-backend.googleapis.com` in `scripts/setup_gcp.sh` is correct (typically `geocoding.googleapis.com`).
- [ ] **Time Zone API:** Decide if the "Live Time" feature (Maps Time Zone API) should be implemented in the solution to replace the mocked "9:00 AM" mentioned in `teachers_prep.md`.
- [ ] **Earth Engine Purge:** Ensure `scripts/setup_gcp.sh` does not mention Earth Engine if it's no longer used.

## 5. Technical Polish & CI/CD
- [ ] **CI/CD Pipeline:** Add a GitHub Actions workflow (`.github/workflows/python-tests.yml`) to automatically run `pytest` and `ruff` on every pull request.
- [ ] **Test Coverage:** Ensure all services (especially the new ADK-based `control_tower.py`) have 100% test coverage in the `solution` branch.
- [ ] **Starter vs. Solution:** Clearly document the branch strategy (e.g., `main` is the starter, `solution` is the completed project) in the `README.md`.

## 6. Visuals
- [ ] **Screenshots:** The `assets/` directory has placeholders (e.g., `dummy_firestore.png`). These should be replaced with real, high-quality screenshots from the actual running application.
- [ ] **Demo GIF:** Add a high-quality GIF of the simulator in action to the top of the `README.md`.
