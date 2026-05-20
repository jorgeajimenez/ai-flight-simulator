# ✈️ Infinite Flight Simulator

[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com)
[![Gemini](https://img.shields.io/badge/Gemini%202.5%20Flash-8E75B2?style=for-the-badge&logo=google-gemini&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![Imagen](https://img.shields.io/badge/Imagen%203-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/vertex-ai/docs/generative-ai/image/generate-images)

Welcome to the AI Flight Simulator repository! In this project, you will transform a silent 3D flight simulator into a multimodal, AI-powered experience using the **Essential 6 Google Cloud Stack**.

## 📖 Codelab Guide
The complete, step-by-step instructions for this project are located in the **[`/codelab`](./codelab/index.md)** directory. 


## 🎫 The Ticket-Driven AI Philosophy
This repository is designed around a core philosophy: **AI Agents work best when given atomic, well-specified tickets.** 

Rather than asking an LLM to "build a flight simulator," we deconstruct the architecture into specialized services and provide strict engineering contracts. You will find the exact specifications for the AI features in the `/tickets` directory. We encourage you to open these markdown files to see how we define clear constraints, expected return formats, and required tool bindings before writing any code.

## 🛠️ Tech Stack
- **Backend:** Python 3.12, Flask
- **Frontend:** CesiumJS (3D Geospatial Engine)
- **AI Models:** Gemini 2.5 Flash (Architect), Imagen 3 (Painter)
- **SDKs:** `google-cloud-aiplatform`, `google-cloud-secret-manager`, `google-cloud-texttospeech`, `google-adk`
- **Infrastructure:** Google Cloud Vertex AI, Secret Manager, Maps Platform

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have the following installed:
- [Python 3.12+](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv) (for fast dependency management)
- [Google Cloud CLI (gcloud)](https://cloud.google.com/sdk/docs/install)

### 2. Setup
```bash
# Clone the repository
git clone https://github.com/jorgeajimenez/ai-flight-simulator.git
cd ai-flight-simulator

# Synchronize dependencies
uv sync

# Enable APIs and setup Secret Manager
chmod +x scripts/setup_gcp.sh
./scripts/setup_gcp.sh
```

### 3. Run the Simulator
```bash
uv run app.py
```
Open your browser to `http://localhost:8080` to start flying!


### Accessing the Completed Solution
If you get stuck or want to review the completed backend architecture, the finalized code is preserved on the `solution` branch. You can check it out at any time:

```bash
git fetch origin
git checkout solution
```

## 🧪 Verification
Each module in the codelab includes a programmatic verification step using `pytest`.
```bash
uv run pytest tests/test_geospatial.py  # Verify Ticket 1
uv run pytest tests/test_ai_vision.py   # Verify Ticket 2
```

## 🛡️ License
Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.
