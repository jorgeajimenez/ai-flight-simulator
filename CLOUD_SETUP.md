# Google Cloud & Billing Setup Guide

Welcome to the Cloud Setup Guide! This document explains **what** we are building, **why** we need Google Cloud, **how much** it costs, and **how** to set it up—whether you are on Mac, Linux, or Windows.

---

## 🧠 What is going on?

The **Infinite Flight Simulator** uses advanced Artificial Intelligence to dynamically re-texture the Earth as you fly over it. To do this, it needs two major services from Google Cloud:

1.  **[Google Earth Engine](https://earthengine.google.com/):** We use this API to fetch real, high-resolution satellite imagery of the ground you are flying over.
2.  **[Vertex AI](https://cloud.google.com/vertex-ai):** We use Google's enterprise AI platform (specifically the `imagegeneration@006` model) to take that real satellite image and a text prompt (like "Cyberpunk City") to generate a brand new, themed texture in real-time.

To use these powerful tools securely, you need a **Google Cloud Project**. This project acts as a container for your APIs, your billing information, and your **Service Account Key** (a secure file acting as a "password" for your simulator to talk to Google).

---

## 💳 What will be billed? (Pricing & Free Tier)

**Good News:** If you are a new Google Cloud user, you are eligible for **[$300 in free credits](https://cloud.google.com/free)** over 90 days, which is more than enough to run this simulator for hundreds of hours.

If you don't have free credits, here is what you are paying for:
*   **Vertex AI Image Generation:** You are charged per image generated. Using standard models, it usually costs around **$0.03 per image**. Since the simulator generates a new patch of terrain occasionally as you fly, costs can accumulate if you fly around for hours, but a standard 10-minute demo session might cost around $0.50 to $1.00.
*   **Google Earth Engine:** Generally free for non-commercial research and development, but commercial API usage is billed by compute time and data egress. For this demo, costs are negligible.

*Note: Google Cloud requires a credit card to verify identity, but you will **not** be automatically charged when your free trial ends unless you manually upgrade your account.*

---

## 🚀 Setup Instructions

We provide automated scripts to make setup extremely easy, regardless of your operating system.

### Option 1: Automated Setup via Script (Recommended)

First, you must install the **[Google Cloud CLI (`gcloud`)](https://cloud.google.com/sdk/docs/install)**. This is a command-line tool that lets you manage Google Cloud.

**For Mac / Linux:**
1. Open your Terminal.
2. Log in with an account that has billing permissions:
   ```bash
   gcloud auth login
   ```
3. Run the setup script:
   ```bash
   bash setup_gcp.sh
   ```

**For Windows:**
1. Open **PowerShell** as an Administrator.
2. Log in to Google Cloud:
   ```powershell
   gcloud auth login
   ```
3. You may need to bypass the execution policy to run the script. Run the PowerShell script:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force
   .\setup_gcp.ps1
   ```

*The script will automatically walk you through linking a billing account, creating a project, enabling the APIs, and downloading your secure `service-account-key.json` file.*

---

## 🧭 Walkthrough: Verifying your Setup

Once you have completed the setup (automated or manual), here is how to verify everything is correct:

1.  **Check for the Key:** You should see a file named `service-account-key.json` in your project folder.
2.  **Verify the Project ID:** Open `service-account-key.json` and verify the `"project_id"` matches the one you created.
3.  **Test Earth Engine:** Some accounts require a one-time registration for Earth Engine. Visit [earthengine.google.com/signup](https://earthengine.google.com/signup) and ensure your account is registered. If it's a new cloud project, you might need to select it from the dropdown on that page.

---

## 🛠 Troubleshooting

### ❌ Error: "IAM Permission Denied"
**The Problem:** The simulator starts, but image generation fails with a 403 error.
**The Fix:** 
1. Go to **IAM & Admin > IAM** in the Cloud Console.
2. Find your service account (ending in `@...iam.gserviceaccount.com`).
3. Click the pencil icon to edit.
4. Ensure it has **Vertex AI User** and **Earth Engine Resource Viewer**.

### ❌ Error: "Cloud Billing Not Enabled"
**The Problem:** The setup script fails while enabling APIs.
**The Fix:**
1. Go to **Billing** in the Cloud Console.
2. Click **My Projects**.
3. Ensure your project has a billing account linked in the "Billing Account" column. If not, click the three dots and select **Change Billing**.

### ❌ Error: "Vertex AI API Not Enabled"
**The Problem:** The backend logs show an error about `aiplatform.googleapis.com`.
**The Fix:**
1. Go to **APIs & Services > Library**.
2. Search for "Vertex AI API".
3. If it says "Enable", click it. It can take up to 5 minutes to propagate.

---

## Option 2: Manual Setup via Google Cloud Console

If you prefer to set this up manually without the command line, follow these steps in your browser:

### 1. Set Up Google Cloud Billing
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Open the Navigation menu (top left) and select **Billing**.
3. Click **Link a billing account** or **Manage billing accounts**, then click **Create Account**. Follow the prompts.

### 2. Create a New Google Cloud Project
1. In the Cloud Console, click the **Project drop-down** at the top.
2. Click **New Project**. Name it (e.g., `infinite-flight-simulator`) and select your Billing Account.
3. Click **Create** and ensure the new project is selected. *(Write down your Project ID!)*

### 3. Enable Required APIs
1. Go to **APIs & Services** > **Library** in the menu.
2. Search for **Vertex AI API** and click **Enable**.
3. Search for **Google Earth Engine API** and click **Enable**.

### 4. Create a Service Account and Generate a Key
1. Go to **IAM & Admin** > **Service Accounts**.
2. Click **Create Service Account**. Name it `flight-sim-backend` and click Continue.
3. **Assign Roles:** Add the following roles:
   *   **Vertex AI User**
   *   **Earth Engine Resource Viewer**
4. Click **Continue**, then **Done**.
5. Click on the email address of your new service account, go to the **Keys** tab, click **Add Key** > **Create new key**.
6. Select **JSON** and click **Create**. The key will download.

### 5. Final Step: Place the Keys

You have two keys to set up:

1.  **Service Account Key (Backend):** Rename the downloaded JSON file to exactly `service-account-key.json` and move it into the root folder of the `infinite-loop-simulator` project.
2.  **API Key (Frontend):** Go to **APIs & Services** > **Credentials**. Click **Create Credentials** > **API key**. Copy this key. Instead of putting this in a `.env` file or hardcoding it, we use **Google Cloud Secret Manager** to keep it secure. Run these commands in your terminal:

```bash
# Enable Secret Manager
gcloud services enable secretmanager.googleapis.com

# Create the secret
gcloud secrets create GOOGLE_MAPS_API_KEY --replication-policy="automatic"

# Add your API key
echo -n "YOUR_COPIED_API_KEY" | gcloud secrets versions add GOOGLE_MAPS_API_KEY --data-file=-
```

You are now ready to start the server! Return to the [README.md](./README.md) for instructions.