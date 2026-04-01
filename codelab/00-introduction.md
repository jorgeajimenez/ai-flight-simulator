# Module 0: Welcome to Infinite Flight

Welcome to the **"Build with AI"** 3D Flight Simulator workshop! We are thrilled to have you here.

## 🛩️ The Mission

You have just inherited a legacy, browser-based 3D flight simulator built with CesiumJS and vanilla JavaScript. It looks incredible, but under the hood, it's a monolithic script that lacks intelligence and crashes the browser's V8 engine if it loads too many 3D photorealistic tiles. 

Your mission today is to **give this simulator a brain**. 

You will deconstruct the backend into a modern, enterprise-grade **Service-Oriented Architecture (SOA)** and infuse it with Google Cloud's most advanced Generative AI models.

![The Infinite Flight Simulator](./assets/intro_screenshot.png)

*The flight simulator in action. By the end of this codelab, you will be able to terraform the terrain beneath you using multimodal AI.*

---

## 🧠 The "Essential 6" Tech Stack

Instead of just chatting with an LLM in a text box, you are going to learn how to build a **multimodal, agentic system** grounded in physical reality. To do this, we will use six core Google Cloud technologies:

1.  **Secret Manager (Zero-Trust Security):** We will rip out all hardcoded API keys and establish a secure credential vault.
2.  **Google Earth Engine (Physical Grounding):** We will stream raw Copernicus Sentinel-2 satellite data to mathematically anchor our AI to the real world, preventing "spatial hallucinations."
3.  **Vertex AI (Visual RAG):** We will build a two-stage generative pipeline. **Gemini 2.5 Flash** will act as our prompt-engineering analyst, and **Imagen 3** will act as our painter, terraforming the 3D map in real-time.
4.  **Cloud Text-to-Speech (Immersive Audio):** We will synthesize real-time, high-fidelity pilot and Air Traffic Control advisories.
5.  **Cloud Storage (Asset CDN):** We will host our generated AI textures globally.
6.  **Cloud Firestore (Agentic Memory):** We will create a persistent "Anomaly Tracker" database, allowing pilots globally to see what others have terraformed.

---

## 🤖 The Grand Finale: Agentic Intelligence

In the final module, you won't just be making API calls. You will build an **Autonomous Air Traffic Control Agent** using Vertex AI Function Calling. 

When a pilot clicks "WHERE AM I?", your Gemini agent will autonomously pause, use tools to scan the Firestore database and identify geographical landmarks, and synthesize a dynamic audio briefing about the anomalies in the area.

## 🎒 Prerequisites

Before we begin, ensure you have:
*   A Google Cloud account.
*   An active **Billing Account** linked to a Google Cloud Project (Generative AI endpoints and Earth Engine require active billing).
*   A "Build with AI" mindset!

Are you ready? Let's take flight. Move on to **[Module 1: Cloud Setup & Initial Generation](./01-cloud-setup.md)**.
