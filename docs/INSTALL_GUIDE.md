# Installation Guide

Here is a comprehensive list of everything you need to install on your local machine to run the **Infinite Flight Simulator** workshop demo.

## Core System Requirements

1. **Git**
   - **Why:** To clone this repository.
   - **Install:** [https://git-scm.com/downloads](https://git-scm.com/downloads)

2. **Google Cloud CLI (`gcloud`)**
   - **Why:** Required to run the automated Cloud and Billing setup scripts (`scripts/setup_gcp.sh`) to easily authenticate and get your Service Account key.
   - **Install:** [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)

3. **`uv` (Python Package Manager)**
   - **Why:** Used for lightning-fast Python dependency installation and environment management. It will also automatically download the correct Python version (3.12) required for the backend.
   - **Install (Mac/Linux):** `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - **Install (Windows):** `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
   - **Full Instructions:** [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

4. **A Modern Web Browser**
   - **Why:** To run the WebGL-powered CesiumJS 3D flight simulator.
   - **Requirement:** Chrome, Firefox, Edge, or Safari (updated to a recent version).

---

## Python Dependencies

You do **not** need to install these manually. When you run the start command from the `README.md` (`uv run --python 3.12 ...`), `uv` will automatically download and install these in an isolated environment based on the `requirements.txt`:

- `flask==3.0.2` (Web server to serve the frontend and proxy requests)
- `requests==2.31.0` (For HTTP requests)
- `earthengine-api==0.1.391` (To fetch real-world terrain textures)
- `google-cloud-aiplatform==1.42.1` (Vertex AI SDK to perform image-to-image terraforming)
