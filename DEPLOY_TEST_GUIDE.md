# 🚀 Quick Deployment & Verification Guide

**Purpose:** This guide is for verifying that the fully completed codebase deploys and runs successfully in a fresh Google Cloud environment. It skips all codelab and coding steps, focusing purely on infrastructure setup, API wiring, and final application testing.

---

### Step 1: The Clean Slate 
To ensure no hidden permissions or cached configurations are masking bugs, use a fresh Google Cloud project or a secondary Google account.

1. Open an **Incognito / Private Browsing** window.
2. Log into Google with your test/admin account.
3. Go to [console.cloud.google.com](https://console.cloud.google.com/).
4. **Billing Check:** Ensure a billing account is active.
5. Click the **Activate Cloud Shell** icon (the terminal prompt `>_` in the top right corner).

---

### Step 2: Workspace Prep (Inside Cloud Shell)
Cloud Shell is an ephemeral Linux VM. We need to get the code and our package manager (`uv`) installed.

1. **Install `uv`:** Cloud Shell doesn't have `uv` by default. Run this to install it:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source $HOME/.local/bin/env
   ```

2. **Clone the Repository:**
   ```bash
   git clone https://github.com/jorgeajimenez/ai-flight-simulator.git
   cd ai-flight-simulator
   # Note: Ensure you are on the branch that contains the completed code.
   ```

---

### Step 3: Running the Automated Setup
Because Cloud Shell is pre-authenticated, the script will skip the login step and go straight to project creation and API enablement.

1. **Enable Deployment APIs:** Run this command first to ensure all required services are active:
   ```bash
   gcloud services enable \
       run.googleapis.com \
       artifactregistry.googleapis.com \
       cloudbuild.googleapis.com \
       aiplatform.googleapis.com \
       compute.googleapis.com \
       secretmanager.googleapis.com \
       texttospeech.googleapis.com \
       firestore.googleapis.com \
       earthengine.googleapis.com
   ```

2. Execute the setup script:
   ```bash
   bash setup_gcp.sh
   ```
2. **Follow the prompts:**
   - Create a unique project ID (e.g., `gdg-deploy-test-001`).
   - Select the billing account ID.
   - When prompted for the Maps API Key, you can press Enter to skip for now, OR go grab a key from your console.

---

### Step 4: The "Manual Magic" (Crucial Console Steps)
These are the steps the script *cannot* do for security/legal reasons. You must verify these work.

1. **Earth Engine Registration:**
   - Go to [earthengine.google.com/non-commercial/](https://earthengine.google.com/non-commercial/).
   - Register the account for "Unpaid/Non-commercial" use.
   - *Note: If skipped, the Geospatial API throws a 403 Forbidden error during terraforming.*

2. **Google Maps 3D Tiles Handshake:**
   - Go to the [Google Maps Platform Console](https://console.cloud.google.com/google/maps-apis/overview).
   - Click "Get Started" (if it's a new account, confirm billing details).
   - Search for **"Photorealistic 3D Tiles"** in the APIs library and click **Enable**.
   - Go to the "Credentials" tab, copy the API Key.

3. **Secret Manager:**
   - Go to [Secret Manager](https://console.cloud.google.com/security/secret-manager).
   - Create a secret named `GOOGLE_MAPS_API_KEY` and paste your Google Maps API key.

---

### Step 5: Start the Server & Verify
With the complete code already in the repository and the infrastructure wired up, you can immediately test the application.

1. **Install Python dependencies:**
   ```bash
   uv sync
   ```
2. **The Icebreaker / CLI Test:** Verify backend API connectivity.
   ```bash
   uv run python generate_texture.py "glowing neon steampunk"
   ```
   *Check if `assets/texture.svg` was generated successfully without auth errors.*
3. **Start the backend server:**
   ```bash
   uv run python app.py
   ```
4. **The Web Preview Test:**
   - In the top right of the Cloud Shell terminal pane, click the **Web Preview** icon.
   - Click **Preview on port 8080**.
5. **The Final Verification Checklist:**
   - [ ] **Maps:** Do the 3D buildings load instantly upon opening the preview? 
   - [ ] **Terraform (Vision/Earth Engine/TTS):** Click "Transform Area". Does the audio play, and does the terrain change to a Cyberpunk city?
   - [ ] **ADK (Anomaly Tracker):** Fly somewhere else, click "WHERE AM I?". Does the ATC agent warn you about the Cyberpunk anomaly you just created?

---

### Step 6: Teardown
Once you are satisfied the deployment test was successful, destroy the test project so you aren't charged for idle resources (like Firestore or Secret Manager).

```bash
gcloud projects delete gdg-deploy-test-001
```
