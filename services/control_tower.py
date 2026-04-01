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
