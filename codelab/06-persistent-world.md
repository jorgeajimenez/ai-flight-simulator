# Module 6: Agentic Intelligence & The Anomaly Tracker

In this final module, we build an **Autonomous Agent** alongside a **Persistent World State Sync** service to share terraforming events globally using Firestore.

## Why an Agent?
Instead of hardcoding the "WHERE AM I?" response, we give Gemini 2.5 Flash access to **Tools** via Vertex AI Function Calling (ADK). The `ControlTowerAgent` will autonomously decide to:
1.  **Visually identify** the landmark below the pilot.
2.  **Scan the Firestore database** for recent terraforming "anomalies" created by other pilots globally.

![Architecture: Persistent World Agent](./assets/06_persistent_world.png)

*This architecture illustrates the Agentic workflow. The Gemini 2.5 Flash agent receives the pilot's query and autonomously decides which tools to invoke before synthesizing a context-aware response.*

---

## Implementation: `ControlTowerAgent`

**Action Marker 6.1:** Terminate the Flask server (CTRL+C). Open `services/control_tower.py`, locate the `[CODELAB STEP 6C]` marker, and paste the following Agentic implementation using the unified `google-genai` SDK.

```python
from google import genai
from google.genai import types
from config import GCPConfig
from services.state_sync import PersistentWorldClient

class ControlTowerAgent:

    @staticmethod
    def contact_tower(lat: float, lon: float) -> str:
        client = genai.Client(
            vertexai=True,
            project=GCPConfig.PROJECT_ID,
            location=GCPConfig.LOCATION
        )

        # 1. Tool Schema Definition
        get_telemetry_tool = types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name="get_telemetry",
                    description="Get the current geographical landmark name at these coordinates.",
                    parameters={
                        "type": "OBJECT",
                        "properties": {
                            "lat": {"type": "NUMBER"},
                            "lon": {"type": "NUMBER"}
                        }
                    }
                )
            ]
        )

        scan_anomaly_tool = types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name="scan_anomaly_tracker",
                    description="Scan the persistent world for terraforming anomalies nearby.",
                    parameters={
                        "type": "OBJECT",
                        "properties": {
                            "lat": {"type": "NUMBER"},
                            "lon": {"type": "NUMBER"}
                        }
                    }
                )
            ]
        )

        # 2. Agent Initialization
        model = client.models.create_chat_session(
            model='gemini-2.5-flash',
            config=types.GenerateContentConfig(
                tools=[get_telemetry_tool, scan_anomaly_tool],
                temperature=0.3
            )
        )

        initial_prompt = f"Pilot requesting telemetry and anomaly scan at Coordinates: {lat}, {lon}."
        response = model.send_message(initial_prompt)

        # 3. The Execution Loop
        if response.function_calls:
            function_responses = []
            for function_call in response.function_calls:
                if function_call.name == "get_telemetry":
                    # Simulated geocoding for demonstration
                    result = {"status": "success", "location": "Unknown Sector"}
                    function_responses.append(
                        types.Part.from_function_response(name="get_telemetry", response=result)
                    )
                elif function_call.name == "scan_anomaly_tracker":
                    anomalies = PersistentWorldClient.scan_vicinity(lat, lon)
                    function_responses.append(
                        types.Part.from_function_response(name="scan_anomaly_tracker", response={"anomalies": anomalies})
                    )
            
            final_response = model.send_message(function_responses)
            return final_response.text

        return response.text
```

**Action Marker 6.2:** Restart the Flask server (`uv run app.py`).

---

## 🛠 Troubleshooting Firestore

If you get a database error when saving or scanning the anomaly tracker:

*   **Firestore Initialization:** Go to the **Firestore** section in the Google Cloud Console. Click **Create Database** and ensure you select **Native Mode**.

<br><span style="color:red; font-weight:bold;">📸 TAKE SCREENSHOT: The Firestore setup wizard showing 'Native Mode' selected. Save as `assets/dummy_firestore.png`</span>
