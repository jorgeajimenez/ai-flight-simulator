<#
.SYNOPSIS
Automated Google Cloud setup script for Infinite Flight Simulator

.DESCRIPTION
This PowerShell script sets up a Google Cloud project (new or existing), links it to a billing account,
enables necessary APIs (Vertex AI, Earth Engine, Secret Manager), creates a service account,
assigns roles, and generates a service-account-key.json file.
#>

$ErrorActionPreference = "Stop"

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host " Infinite Flight Simulator: Google Cloud Setup Script" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# Check if gcloud is installed
if (!(Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: Google Cloud CLI (gcloud) is not installed." -ForegroundColor Red
    Write-Host "Please install it first: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Google Cloud CLI is installed." -ForegroundColor Green

# Ensure user is authenticated
try {
    $null = gcloud auth print-access-token 2>&1
} catch {
    Write-Host "🔑 Please log in to Google Cloud:" -ForegroundColor Yellow
    gcloud auth login
}

Write-Host "✅ Authenticated with Google Cloud." -ForegroundColor Green
Write-Host ""

# Fetch existing projects
Write-Host "Fetching your Google Cloud projects..." -ForegroundColor Cyan
$PROJECT_LIST = @(gcloud projects list --format="value(projectId)" | Where-Object { $_ -match "\S" })

if ($PROJECT_LIST.Count -eq 0) {
    Write-Host "No existing projects found. Let's create a new one." -ForegroundColor Yellow
    $PROJECT_CHOICE = 'n'
} else {
    Write-Host "Available Projects:" -ForegroundColor Yellow
    for ($i = 0; $i -lt $PROJECT_LIST.Count; $i++) {
        Write-Host "  $($i+1)) $($PROJECT_LIST[$i])"
    }
    Write-Host "  n) Create a NEW project"
    Write-Host ""
    $PROJECT_CHOICE = Read-Host "Select a project by number or 'n' for new"
}

if ($PROJECT_CHOICE -eq 'n' -or $PROJECT_CHOICE -eq 'N') {
    $PROJECT_ID = Read-Host "Enter a NEW Google Cloud Project ID (must be globally unique, e.g., flight-sim-1234)"

    if ([string]::IsNullOrWhiteSpace($PROJECT_ID)) {
        Write-Host "❌ Error: Project ID cannot be empty." -ForegroundColor Red
        exit 1
    }

    Write-Host "🚀 Creating project: $PROJECT_ID..." -ForegroundColor Cyan
    gcloud projects create "$PROJECT_ID" --name="Infinite Flight Simulator"

    Write-Host "✅ Project created." -ForegroundColor Green
    Write-Host ""

    # Link billing account
    Write-Host "💳 Fetching available billing accounts..." -ForegroundColor Cyan
    $BILLING_ACCOUNTS = gcloud billing accounts list --format="value(name,displayName)"

    if ([string]::IsNullOrWhiteSpace($BILLING_ACCOUNTS)) {
        Write-Host "❌ Error: No billing accounts found. Please create one at https://console.cloud.google.com/billing" -ForegroundColor Red
        exit 1
    }

    Write-Host "Available Billing Accounts:" -ForegroundColor Yellow
    gcloud billing accounts list
    Write-Host ""
    $BILLING_ID = Read-Host "Enter the ACCOUNT_ID of the billing account to link to this project"

    if ([string]::IsNullOrWhiteSpace($BILLING_ID)) {
        Write-Host "❌ Error: Billing ID cannot be empty." -ForegroundColor Red
        exit 1
    }

    Write-Host "🔗 Linking billing account..." -ForegroundColor Cyan
    gcloud billing projects link "$PROJECT_ID" --billing-account="$BILLING_ID"

    Write-Host "✅ Billing account linked." -ForegroundColor Green
    Write-Host ""
} else {
    $choiceInt = 0
    if ([int]::TryParse($PROJECT_CHOICE, [ref]$choiceInt) -and $choiceInt -ge 1 -and $choiceInt -le $PROJECT_LIST.Count) {
        $PROJECT_ID = $PROJECT_LIST[$choiceInt - 1]
        Write-Host "✅ Using existing project: $PROJECT_ID" -ForegroundColor Green
        Write-Host ""
    } else {
        Write-Host "❌ Error: Invalid selection." -ForegroundColor Red
        exit 1
    }
}

# Set project as default
gcloud config set project "$PROJECT_ID"

# Enable APIs
Write-Host "⚡ Enabling Vertex AI, Earth Engine, and Secret Manager APIs..." -ForegroundColor Cyan
gcloud services enable aiplatform.googleapis.com
gcloud services enable earthengine.googleapis.com
gcloud services enable secretmanager.googleapis.com

Write-Host "⚠️ Note: The Google Maps Photorealistic 3D Tiles API must often be enabled manually in the Cloud Console due to specific Terms of Service." -ForegroundColor Yellow
Write-Host "✅ Core APIs enabled." -ForegroundColor Green
Write-Host ""

# Check Maps API Status safely
Write-Host "🗺️ Checking Google Maps Platform APIs..." -ForegroundColor Cyan
$ENABLED_SERVICES = gcloud services list --enabled --format="value(config.name)"
if ($ENABLED_SERVICES -match "maps-backend.googleapis.com") {
    Write-Host "✅ Google Maps API is already enabled!" -ForegroundColor Green
} else {
    Write-Host "⚠️ Google Maps API is NOT enabled yet." -ForegroundColor Yellow
    Write-Host "   You must enable it manually in the Cloud Console due to specific Terms of Service:" -ForegroundColor Yellow
    Write-Host "   👉 https://console.cloud.google.com/apis/library/maps-backend.googleapis.com" -ForegroundColor Yellow
}
Write-Host ""

# Manage Google Maps API Key Secret
Write-Host "🗺️ We need your Google Maps API Key to store securely in Secret Manager." -ForegroundColor Cyan
Write-Host "You can get one at: https://console.cloud.google.com/google/maps-apis/credentials" -ForegroundColor Yellow
$MAPS_API_KEY = Read-Host "Enter your Google Maps API Key"

if ([string]::IsNullOrWhiteSpace($MAPS_API_KEY)) {
    Write-Host "⚠️ Warning: No API Key provided. The 3D map will not load until you add it to Secret Manager manually." -ForegroundColor Yellow
} else {
    Write-Host "🔒 Saving API Key to Secret Manager..." -ForegroundColor Cyan
    try {
        $null = gcloud secrets describe GOOGLE_MAPS_API_KEY 2>&1
    } catch {
        gcloud secrets create GOOGLE_MAPS_API_KEY --replication-policy="automatic"
    }
    
    # Add the value as a new version
    $MAPS_API_KEY | Out-File -FilePath "temp_maps_key.txt" -NoNewline
    gcloud secrets versions add GOOGLE_MAPS_API_KEY --data-file="temp_maps_key.txt"
    Remove-Item "temp_maps_key.txt" -Force
    Write-Host "✅ API Key securely saved." -ForegroundColor Green
}
Write-Host ""

# Create Service Account
$SA_NAME = "flight-sim-backend"
$SA_EMAIL = "${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

Write-Host "🤖 Checking/Creating Service Account: $SA_NAME..." -ForegroundColor Cyan
try {
    $null = gcloud iam service-accounts describe "$SA_EMAIL" 2>&1
    Write-Host "Service account already exists, skipping creation." -ForegroundColor Yellow
} catch {
    gcloud iam service-accounts create "$SA_NAME" `
        --description="Backend service account for Infinite Flight Simulator" `
        --display-name="Flight Sim Backend"
}

# Assign Roles
Write-Host "🔐 Assigning roles (Vertex AI User, Earth Engine Resource Viewer, Secret Accessor)..." -ForegroundColor Cyan
Start-Sleep -Seconds 5 # Wait for SA to propagate

gcloud projects add-iam-policy-binding "$PROJECT_ID" `
    --member="serviceAccount:$SA_EMAIL" `
    --role="roles/aiplatform.user" > $null

gcloud projects add-iam-policy-binding "$PROJECT_ID" `
    --member="serviceAccount:$SA_EMAIL" `
    --role="roles/earthengine.viewer" > $null

gcloud projects add-iam-policy-binding "$PROJECT_ID" `
    --member="serviceAccount:$SA_EMAIL" `
    --role="roles/secretmanager.secretAccessor" > $null

Write-Host "✅ Roles assigned." -ForegroundColor Green
Write-Host ""

# Generate Key
Write-Host "🔑 Generating service-account-key.json..." -ForegroundColor Cyan
if (Test-Path "service-account-key.json") {
    Write-Host "⚠️ Existing service-account-key.json found. Backing it up to service-account-key.json.bak" -ForegroundColor Yellow
    Rename-Item -Path "service-account-key.json" -NewName "service-account-key.json.bak" -Force
}

gcloud iam service-accounts keys create service-account-key.json `
    --iam-account="$SA_EMAIL"

Write-Host ""
Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host "Your service account key has been saved as 'service-account-key.json'." -ForegroundColor Yellow
Write-Host "You can now run the simulator." -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
