#!/bin/bash

# setup_gcp.sh
# Automated Google Cloud setup script for Infinite Flight Simulator

set -e

echo "====================================================="
echo " Infinite Flight Simulator: Google Cloud Setup Script"
echo "====================================================="
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: Google Cloud CLI (gcloud) is not installed."
    echo "Please install it first: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo "✅ Google Cloud CLI is installed."

# Ensure user is authenticated
if ! gcloud auth print-access-token &> /dev/null; then
    echo "🔑 Please log in to Google Cloud:"
    gcloud auth login
fi

echo "✅ Authenticated with Google Cloud."
echo ""

# Fetch existing projects
echo "Fetching your Google Cloud projects..."
PROJECT_LIST=()
while IFS= read -r line; do
    if [ -n "$line" ]; then
        PROJECT_LIST+=("$line")
    fi
done < <(gcloud projects list --format="value(projectId)")

if [ ${#PROJECT_LIST[@]} -eq 0 ]; then
    echo "No existing projects found. Let's create a new one."
    PROJECT_CHOICE="n"
else
    echo "Available Projects:"
    for i in "${!PROJECT_LIST[@]}"; do
        echo "  $((i+1))) ${PROJECT_LIST[$i]}"
    done
    echo "  n) Create a NEW project"
    echo ""
    read -p "Select a project by number or 'n' for new: " PROJECT_CHOICE
fi

if [[ "$PROJECT_CHOICE" == "n" || "$PROJECT_CHOICE" == "N" ]]; then
    read -p "Enter a NEW Google Cloud Project ID (must be globally unique, e.g., flight-sim-1234): " PROJECT_ID
    if [ -z "$PROJECT_ID" ]; then
        echo "❌ Error: Project ID cannot be empty."
        exit 1
    fi

    echo "🚀 Creating project: $PROJECT_ID..."
    gcloud projects create "$PROJECT_ID" --name="Infinite Flight Simulator"
    echo "✅ Project created."
    echo ""

    # Link billing account (only needed for new projects here)
    echo "💳 Fetching available billing accounts..."
    BILLING_ACCOUNTS=$(gcloud billing accounts list --format="value(name,displayName)")

    if [ -z "$BILLING_ACCOUNTS" ]; then
        echo "❌ Error: No billing accounts found. Please create one at https://console.cloud.google.com/billing"
        exit 1
    fi

    echo "Available Billing Accounts:"
    gcloud billing accounts list
    echo ""
    read -p "Enter the ACCOUNT_ID of the billing account to link to this project: " BILLING_ID

    if [ -z "$BILLING_ID" ]; then
        echo "❌ Error: Billing ID cannot be empty."
        exit 1
    fi

    echo "🔗 Linking billing account..."
    gcloud billing projects link "$PROJECT_ID" --billing-account="$BILLING_ID"
    echo "✅ Billing account linked."
    echo ""
else
    if ! [[ "$PROJECT_CHOICE" =~ ^[0-9]+$ ]] || [ "$PROJECT_CHOICE" -lt 1 ] || [ "$PROJECT_CHOICE" -gt ${#PROJECT_LIST[@]} ]; then
        echo "❌ Error: Invalid selection."
        exit 1
    fi
    INDEX=$((PROJECT_CHOICE-1))
    PROJECT_ID="${PROJECT_LIST[$INDEX]}"
    echo "✅ Using existing project: $PROJECT_ID"
    echo ""
fi

# Set project as default
gcloud config set project "$PROJECT_ID"

# Enable APIs
echo "⚡ Enabling Vertex AI, Earth Engine, Text-to-Speech, Firestore, and Secret Manager APIs..."
gcloud services enable aiplatform.googleapis.com
gcloud services enable earthengine.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable texttospeech.googleapis.com
gcloud services enable firestore.googleapis.com

echo "⚠️ Note: The Google Maps Photorealistic 3D Tiles API must often be enabled manually in the Cloud Console due to specific Terms of Service."
echo "✅ Core APIs enabled."
echo ""

# Check Maps API Status safely
echo "🗺️ Checking Google Maps Platform APIs..."
if gcloud services list --enabled --format="value(config.name)" | grep -q "maps-backend.googleapis.com"; then
    echo "✅ Google Maps API is already enabled!"
else
    echo "⚠️ Google Maps API is NOT enabled yet."
    echo "   You must enable it manually in the Cloud Console due to specific Terms of Service:"
    echo "   👉 https://console.cloud.google.com/apis/library/maps-backend.googleapis.com"
fi
echo ""

# Manage Google Maps API Key Secret
echo "🗺️ We need your Google Maps API Key to store securely in Secret Manager."
echo "You can get one at: https://console.cloud.google.com/google/maps-apis/credentials"
read -p "Enter your Google Maps API Key: " MAPS_API_KEY

if [ -z "$MAPS_API_KEY" ]; then
    echo "⚠️ Warning: No API Key provided. The 3D map will not load until you add it to Secret Manager manually."
else
    echo "🔒 Saving API Key to Secret Manager..."
    # Check if secret exists, if not create it
    if ! gcloud secrets describe GOOGLE_MAPS_API_KEY &> /dev/null; then
        gcloud secrets create GOOGLE_MAPS_API_KEY --replication-policy="automatic"
    fi
    
    # Add the value as a new version
    echo -n "$MAPS_API_KEY" | gcloud secrets versions add GOOGLE_MAPS_API_KEY --data-file=-
    echo "✅ API Key securely saved."
fi
echo ""

# Create Service Account
SA_NAME="flight-sim-backend"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

echo "🤖 Checking/Creating Service Account: $SA_NAME..."
if ! gcloud iam service-accounts describe "$SA_EMAIL" &> /dev/null; then
    gcloud iam service-accounts create "$SA_NAME" \
        --description="Backend service account for Infinite Flight Simulator" \
        --display-name="Flight Sim Backend"
else
    echo "Service account already exists, skipping creation."
fi

# Assign Roles
echo "🔐 Assigning roles (Vertex AI User, Earth Engine Viewer, Secret Accessor, Service Usage Consumer)..."
sleep 5 # Wait for SA to propagate
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/aiplatform.user" > /dev/null

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/earthengine.viewer" > /dev/null

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/secretmanager.secretAccessor" > /dev/null

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/serviceusage.serviceUsageConsumer" > /dev/null

echo "✅ Roles assigned."
echo ""

# Generate Key
echo "🔑 Generating service-account-key.json..."
if [ -f "service-account-key.json" ]; then
    echo "⚠️ Existing service-account-key.json found. Backing it up to service-account-key.json.bak"
    mv service-account-key.json service-account-key.json.bak
fi

gcloud iam service-accounts keys create service-account-key.json \
    --iam-account="$SA_EMAIL"

echo ""
echo "🎉 Setup Complete!"
echo "Your service account key has been saved as 'service-account-key.json'."
echo "You can now run the simulator."
echo "====================================================="
