# Build with AI: Infinite Flight Simulator

> **⚠️ ATTENTION:** You are currently on the **STARTER** branch. This codebase contains `TODO` markers where you will implement the AI logic.

A browser-based 3D flight simulator built with vanilla JavaScript, CesiumJS, and a Flask backend integrating Vertex AI for dynamic terraforming. It specifically demonstrates "Infinite Loop" memory architecture to survive rendering massive 3D Photorealistic Google Maps tiles without crashing the browser's V8 engine.

## 🚀 Getting Started

1.  **System Requirements & Setup:** Review the **[INSTALL_GUIDE.md](./docs/INSTALL_GUIDE.md)** for tool installation and **[CLOUD_SETUP.md](./docs/CLOUD_SETUP.md)** for your Google Cloud project configuration.
2.  **Codelab:** Follow the markdown guides in the `/codelab` directory to implement the missing modules.

### Start the Server

This project uses Python and `uv`. Run the Flask app directly:

```bash
uv run app.py
```
