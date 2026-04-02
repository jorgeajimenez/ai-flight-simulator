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
    
    BILLING_IDS=()
    BILLING_NAMES=()
    while IFS=$'\t' read -r id name; do
        if [ -n "$id" ]; then
            # Remove 'billingAccounts/' prefix if present
            id=${id#billingAccounts/}
            BILLING_IDS+=("$id")
            BILLING_NAMES+=("$name")
        fi
    done < <(gcloud billing accounts list --format="value(name,displayName)")

    if [ ${#BILLING_IDS[@]} -eq 0 ]; then
        echo "❌ Error: No billing accounts found. Please create one at https://console.cloud.google.com/billing"
        exit 1
    fi

    if [ ${#BILLING_IDS[@]} -eq 1 ]; then
        BILLING_ID="${BILLING_IDS[0]}"
        echo "✅ Auto-selecting the only available billing account: ${BILLING_NAMES[0]} ($BILLING_ID)"
    else
        echo "Available Billing Accounts:"
        for i in "${!BILLING_IDS[@]}"; do
            echo "  $((i+1))) ${BILLING_NAMES[$i]} (${BILLING_IDS[$i]})"
        done
        echo ""
        read -p "Select a billing account by number: " BILLING_CHOICE
        
        if ! [[ "$BILLING_CHOICE" =~ ^[0-9]+$ ]] || [ "$BILLING_CHOICE" -lt 1 ] || [ "$BILLING_CHOICE" -gt ${#BILLING_IDS[@]} ]; then
            echo "❌ Error: Invalid selection."
            exit 1
        fi
        
        INDEX=$((BILLING_CHOICE-1))
        BILLING_ID="${BILLING_IDS[$INDEX]}"
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
echo "⚡ Enabling Vertex AI, Secret Manager, Text-to-Speech, Firestore, Map Tiles, and Geocoding APIs (this may take a minute)..."
gcloud services enable \
    aiplatform.googleapis.com \
    secretmanager.googleapis.com \
    texttospeech.googleapis.com \
    firestore.googleapis.com \
    tile.googleapis.com \
    geocoding-backend.googleapis.com

echo "✅ Core APIs enabled."
echo ""

# Manage Google Maps API Key Secret
echo -e "\n====================================================="
echo -e " 🗺️  CRITICAL MANUAL STEP: Google Maps API Configuration"
echo -e "====================================================="
SECRET_EXISTS=false
if gcloud secrets describe GOOGLE_MAPS_API_KEY &> /dev/null; then
    SECRET_EXISTS=true
    if gcloud secrets versions access latest --secret="GOOGLE_MAPS_API_KEY" &> /dev/null; then
        echo "✅ A Google Maps API Key is already stored securely in Secret Manager."
        read -p "Do you want to update it? (y/N): " UPDATE_KEY
        if [[ ! "$UPDATE_KEY" =~ ^[Yy]$ ]]; then
            echo "⏭️ Skipping API Key update."
            MAPS_API_KEY="SKIPPED"
        fi
    fi
fi

if [ -z "$MAPS_API_KEY" ]; then
    echo -e "\nYou must manually enable the 3D Map Tiles API and generate an API key."
    echo -e "\033[1;36mSTEP 1: Enable the Map Tiles API\033[0m"
    echo -e "Please hold CTRL (or CMD on Mac) and click this link to open it in a new tab:"
    echo -e "\033[4;34mhttps://console.cloud.google.com/apis/library/tile.googleapis.com?project=$PROJECT_ID\033[0m"
    echo -e "-> Click the blue \033[1mENABLE\033[0m button.\n"
    
    echo -e "\033[1;36mSTEP 2: Generate your API Key\033[0m"
    echo -e "Please hold CTRL (or CMD on Mac) and click this link to open the Credentials page:"
    echo -e "\033[4;34mhttps://console.cloud.google.com/google/maps-apis/credentials?project=$PROJECT_ID\033[0m"
    echo -e "-> Click \033[1mCreate Credentials\033[0m -> \033[1mAPI Key\033[0m and copy it.\n"

    read -p "Paste your Google Maps API Key here (or press Enter to skip): " MAPS_API_KEY

    if [ -z "$MAPS_API_KEY" ]; then
        echo -e "⚠️  \033[1;33mWarning: No API Key provided. The 3D map will not load until you add it manually.\033[0m"
    else
        echo "🔒 Saving API Key to Secret Manager..."
        if [ "$SECRET_EXISTS" = false ]; then
            gcloud secrets create GOOGLE_MAPS_API_KEY --replication-policy="automatic"
        fi
        echo -n "$MAPS_API_KEY" | gcloud secrets versions add GOOGLE_MAPS_API_KEY --data-file=-
        echo "✅ API Key securely saved."
    fi
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
    # Wait for SA to propagate only if newly created
    sleep 5
else
    echo "Service account already exists, skipping creation."
fi

# Assign Roles
echo "🔐 Assigning roles (Vertex AI User, Secret Accessor, Service Usage Consumer)..."
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/aiplatform.user" > /dev/null

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/secretmanager.secretAccessor" > /dev/null

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/serviceusage.serviceUsageConsumer" > /dev/null

echo "✅ Roles assigned."
echo ""

# Generate Key
echo "🔑 Checking service-account-key.json..."
if [ -f "service-account-key.json" ]; then
    echo "✅ Existing service-account-key.json found."
    read -p "Do you want to generate a new key? (y/N): " GEN_KEY
    if [[ "$GEN_KEY" =~ ^[Yy]$ ]]; then
        echo "Backing up to service-account-key.json.bak"
        mv service-account-key.json service-account-key.json.bak
        gcloud iam service-accounts keys create service-account-key.json \
            --iam-account="$SA_EMAIL"
        echo "✅ New key generated."
    else
        echo "⏭️ Skipping key generation."
    fi
else
    gcloud iam service-accounts keys create service-account-key.json \
        --iam-account="$SA_EMAIL"
    echo "✅ New key generated."
fi

echo ""
echo "🎉 Setup Complete!"
echo "Your service account key has been saved as 'service-account-key.json'."
echo "You can now run the simulator."
echo "====================================================="
