# Module 1: Cloud Setup & Initial Generation

Before building the flight simulator's brain, we need to ensure your environment is correctly wired to Google Cloud. If you are using a brand new Google account, follow these steps exactly.

## Step 1: Account Preparation & Billing

1.  **Billing Account:** You must have an active billing account. Go to the [Google Cloud Billing Console](https://console.cloud.google.com/billing) and ensure a billing account is linked to your current project.
2.  **Activate Cloud Shell:** Click the `>_` terminal icon in the top right of your Google Cloud Console. This is your primary development environment.
3.  **Google Maps Platform:** 
    *   In the Cloud Console search bar, type "Google Maps Platform Credentials".
    *   Click **Create Credentials** -> **API Key** and copy it. You will need this in a moment.
    *   *(Note: The Photorealistic 3D Tiles API must be enabled for this key).*

<br><span style="color:red; font-weight:bold;">📸 TAKE SCREENSHOT: Your Google Cloud Console showing the APIs/Credentials screen. Save as `assets/dummy_enable_apis.png`</span>

## Step 2: Clone & Synchronize

Google Cloud Shell comes pre-configured with the tools you need, including the ultra-fast `uv` Python package manager!

**Action Marker 1.1:** Open your Cloud Shell terminal, clone the project, and synchronize the locked dependencies.

```bash
git clone https://github.com/jorgeajimenez/ai-flight-simulator.git
cd ai-flight-simulator
uv sync
```

## Step 3: Identity & Access Management (IAM)

We've provided a script to automate the creation of your Service Account and the enablement of APIs (Vertex AI, Earth Engine, Secret Manager, TTS).

**Action Marker 1.2:** Run the setup script. When prompted, paste your **Google Maps API Key**.

```bash
bash scripts/setup_gcp.sh
```

<br><span style="color:red; font-weight:bold;">📸 TAKE SCREENSHOT: Open 'Secret Manager' in your GCP Console UI and screenshot the `GOOGLE_MAPS_API_KEY` table. Save as `assets/dummy_secret_manager.png`</span>

## Step 4: Earth Engine Registration (CRITICAL)

If you are using a new Google Cloud account, you **must** manually accept the Earth Engine Terms of Service. If you skip this, your simulator will fail with a `403 Forbidden` error later.

1. Visit **[earthengine.google.com/signup](https://earthengine.google.com/signup)**
2. Click **Register** and accept the terms for your project.

## Step 5: Verification (The Vertex AI Handshake)

Let's verify that the AI is working before touching the code. We will use **Gemini 2.5 Flash** to generate a custom 3D building texture.

**Action Marker 1.3:** Execute the texture verification script.

```bash
uv run python scripts/generate_texture.py "Cyberpunk hacker apartment block..."
```

**Verification:** If you see `Saved texture to assets/texture.svg`, your cloud environment is structurally sound.

---

## Architecture: The Cloud Handshake

The diagram below shows how your Cloud Shell environment is communicating with Vertex AI using the credentials we just generated.

![Architecture: Cloud Handshake](./assets/01_cloud_setup.png)

*Notice how `uv` authenticates via the `service-account-key.json` file we generated in the setup script. This establishes a secure, zero-trust handshake with the Vertex AI API, allowing Gemini 2.5 Flash to generate our initial SVG texture and save it locally to the assets folder. This fundamental auth flow will power the rest of our AI services.*
