# Module 1: Cloud Setup & Initial Generation

Before building the flight simulator's brain, we need to ensure your environment is correctly wired to Google Cloud. If you are using a brand new Google account, follow these steps very carefully.

## Step 1: Account Preparation & Billing

1.  **Billing Account:** You must have an active billing account. Go to the [Google Cloud Billing Console](https://console.cloud.google.com/billing) and ensure a billing account is linked to your current project.
2.  **Activate Cloud Shell:** Click the `>_` terminal icon in the top right of your Google Cloud Console. This is your primary development environment.
3.  **Google Maps Platform:** 
    *   In the Cloud Console search bar, type "Google Maps Platform Credentials".
    *   Click **Create Credentials** -> **API Key** and copy it. You will need this in a moment.
    *   *(Note: The Photorealistic 3D Tiles API must be enabled for this key).*

<br><span style="color:red; font-weight:bold;">📸 TAKE SCREENSHOT: Your Google Cloud Console showing the APIs/Credentials screen. Save as `assets/dummy_enable_apis.png` to replace the placeholder!</span>

## Step 2: Clone & Configure

Run these commands in your Cloud Shell terminal to download the project and install dependencies:

```bash
git clone https://github.com/jorgeajimenez/ai-flight-simulator.git
cd ai-flight-simulator
uv sync
```

We've provided a setup script that creates your Service Account, enables necessary APIs (Vertex AI, Earth Engine, Secret Manager, TTS), and securely stores your Maps API key. Run it now:

```bash
bash scripts/setup_gcp.sh
```
*When prompted, paste your Google Maps API Key. The script will securely lock it inside Google Cloud Secret Manager.*

<br><span style="color:red; font-weight:bold;">📸 TAKE SCREENSHOT: Open 'Secret Manager' in your GCP Console UI and screenshot the `GOOGLE_MAPS_API_KEY` table. Save as `assets/dummy_secret_manager.png` to replace the placeholder!</span>

## Step 3: Earth Engine Registration (CRITICAL)
If you have a new Google Cloud account, you **must** manually accept the Earth Engine Terms of Service before the API will work, even if the script enabled it. 

1. Visit **[earthengine.google.com/signup](https://earthengine.google.com/signup)**
2. Ensure you are logged in with the correct Google account.
3. Click "Register" and accept the terms. If you skip this, your simulator will fail with a `403 Forbidden` error later.

---

## Step 4: Generate Base Texture

Before touching the backend code, let's test that your Vertex AI connection is working. We will use **Gemini 2.5 Flash** to generate a custom 3D building texture that will be used throughout the simulator.

Run the texture generation script:
```bash
uv run python scripts/generate_texture.py "Cyberpunk hacker apartment block..."
```

**Verification:**
If successful, the script will output `Saved texture to assets/texture.svg`. You can click on the `assets/texture.svg` file in the Cloud Shell editor to verify the image was generated. 

---

## Architecture: The Cloud Handshake

The diagram below shows how your Cloud Shell environment is communicating with Vertex AI using the credentials we just generated.

![Architecture: Cloud Handshake](./assets/01_cloud_setup.png)

*Notice how `uv` authenticates via the `service-account-key.json` file we generated in the setup script. This establishes a secure, zero-trust handshake with the Vertex AI API, allowing Gemini 2.5 Flash to generate our initial SVG texture and save it locally to the assets folder. This fundamental auth flow will power the rest of our AI services.*