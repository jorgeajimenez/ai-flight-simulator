# Codelab Refactoring Plan

This document outlines the precise changes to be made to the codelab files on the `solution` branch to align with the "Codelab Redesign Specification" (hardened, deterministic engineering track).

## 🛠️ Precise Change Specification

| Category | File | Change Description |
| :--- | :--- | :--- |
| **Dependencies** | `pyproject.toml` | **Add:** `google-genai` (Unified SDK) and `pydantic` (for JSON schemas). |
| **Module 1** | `codelab/01-cloud-setup.md` | **Add:** Explicit `uv` installation and `$PATH` injection commands. **Add:** Red "Screenshot" markers. |
| **Module 2** | `codelab/02-modular-architecture.md`| **Add:** Explicit `uv run pytest tests/test_vault.py` command. **Update:** Vault implementation with in-memory caching. |
| **Module 3** | `codelab/03-geospatial-engine.md` | **Add:** Bold "Action Markers" for exact file locations. **Add:** 403 Forbidden troubleshooting. |
| **Module 4** | `codelab/04-ai-vision.md` | **Overhaul:** Move to 2-stage (Gemini -> Imagen) pipeline using `google-genai`. **Add:** Pydantic JSON schema code. |
| **Module 5** | `codelab/05-immersive-audio.md` | **Update:** `speaking_rate=1.05` for professional cadence. **Add:** Action Markers. |
| **Module 6** | `codelab/06-persistent-world.md` | **Update:** Agentic loop with `google-genai` Parallel Tool Calling. **Add:** Firestore "Native Mode" guide. |

---

## 📝 Preview: Revamped Module 1 (`codelab/01-cloud-setup.md`)

```markdown
# Module 1: Cloud Setup & Initial Generation

Before building the flight simulator's brain, we need to ensure your environment is correctly wired to Google Cloud. If you are using a new account, follow these steps exactly.

## Step 1: Environment Preparation (Cloud Shell)

Google Cloud Shell provides a pre-configured VM, but it lacks our required package manager, **uv**.

**Action Marker 1.1:** Open the Cloud Shell terminal and execute these commands to install `uv` and fix the binary path.

```bash
# 1. Install the uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Inject the uv binary into your current session path
export PATH="$HOME/.local/bin:$PATH"

# 3. Persist the path for future sessions
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

## Step 2: Clone & Synchronize

**Action Marker 1.2:** Clone the project and synchronize the locked dependencies.

```bash
git clone https://github.com/jorgeajimenez/ai-flight-simulator.git
cd ai-flight-simulator
uv sync
```

## Step 3: Identity & Access Management (IAM)

We've provided a script to automate the creation of your Service Account and the enablement of APIs (Vertex AI, Earth Engine, Secret Manager, TTS).

**Action Marker 1.3:** Run the setup script. When prompted, paste your **Google Maps API Key**.

```bash
bash scripts/setup_gcp.sh
```

<br><span style="color:red; font-weight:bold;">📸 TAKE SCREENSHOT: Open 'Secret Manager' in your GCP Console UI and screenshot the GOOGLE_MAPS_API_KEY table. Save as assets/dummy_secret_manager.png</span>

## Step 4: Earth Engine Registration (CRITICAL)

If you are using a new Google Cloud account, you **must** manually accept the Earth Engine Terms of Service. If you skip this, your simulator will fail with a `403 Forbidden` error later.

1. Visit **[earthengine.google.com/signup](https://earthengine.google.com/signup)**
2. Click **Register** and accept the terms for your project.

## Step 5: Verification (The Vertex AI Handshake)

Let's verify that the AI is working before touching the code. We will use **Gemini 2.5 Flash** to generate a custom 3D building texture.

**Action Marker 1.4:** Execute the texture verification script.

```bash
uv run python scripts/generate_texture.py "Cyberpunk hacker apartment block..."
```

**Verification:** If you see `Saved texture to assets/texture.svg`, your cloud environment is structurally sound.
```
