import json
import traceback
import vertexai
from vertexai.generative_models import GenerativeModel, Tool, FunctionDeclaration, Part
from config import GCPConfig, logger

# Ensure Vertex AI is initialized
vertexai.init(project=GCPConfig.PROJECT_ID, location=GCPConfig.LOCATION)

class ControlTowerAgent:
    """
    Agentic Air Traffic Control using Vertex AI Function Calling.
    """

    @staticmethod
    def contact_tower(lat: float, lon: float) -> str:
        """
        Acts as an intelligent ATC using tool-calling patterns.
        """
        logger.info(f"ATC Agent: Pilot requesting update at {lat}, {lon}")
        
        try:
            # 1. Define the Tools
            get_telemetry = FunctionDeclaration(
                name="get_telemetry",
                description="Fetches current weather and visually identifies the real-world landmark the pilot is flying over.",
                parameters={
                    "type": "object",
                    "properties": {
                        "lat": {"type": "number"},
                        "lon": {"type": "number"}
                    },
                    "required": ["lat", "lon"]
                }
            )
            
            scan_multiverse_activity = FunctionDeclaration(
                name="scan_multiverse_activity",
                description="Queries the multiverse database (Firestore) for recently generated terraforming anomalies (e.g. Cyberpunk or Mars bases).",
                parameters={
                    "type": "object",
                    "properties": {
                        "lat": {"type": "number"},
                        "lon": {"type": "number"}
                    },
                    "required": ["lat", "lon"]
                }
            )
            
            atc_tools = Tool(function_declarations=[get_telemetry, scan_multiverse_activity])
            
            # 2. Initialize Model (Using 2.5 Flash per user mandate)
            model_name = "gemini-2.5-flash"
            agent = GenerativeModel(model_name, tools=[atc_tools])
            
            # 3. Immersive ATC Prompt
            chat = agent.start_chat()
            system_instruction = (
                "You are an Air Traffic Control agent. You MUST use your tools to check visual telemetry AND scan the multiverse radar. "
                "Respond strictly as an ATC (max 30 words). Tell the pilot what landmark they are over. "
                "If the multiverse radar finds recent anomalies (terraforms), warn the pilot about them. Be immersive."
            )
            prompt = f"{system_instruction} Flight 001 at {lat}, {lon} requesting airspace update."
            
            response = chat.send_message(prompt)
            
            # 4. Handle Parallel Tool Calling Loop
            if response.candidates and response.candidates[0].content.parts:
                function_responses = []
                for part in response.candidates[0].content.parts:
                    if part.function_call:
                        fn = part.function_call
                        logger.info(f"ATC Agent: Decided to execute tool -> {fn.name}")
                        
                        if fn.name == "get_telemetry":
                            from services.ai_vision import AIVisionService
                            location_desc = AIVisionService.describe_location(lat, lon)
                            function_responses.append(
                                Part.from_function_response(name=fn.name, response={"content": {"weather": "Winds 12kt North.", "landmark": location_desc}})
                            )
                            
                        elif fn.name == "scan_multiverse_activity":
                            from services.state_sync import GlobalMultiverseClient
                            recent_anomalies = GlobalMultiverseClient.get_recent_activity(lat, lon)
                            function_responses.append(
                                Part.from_function_response(name=fn.name, response={"content": {"recent_anomalies": recent_anomalies}})
                            )
                
                # Send all the tool execution results back to Gemini at once
                if function_responses:
                    response = chat.send_message(function_responses)
                
            return response.text.replace("*", "").strip()
            
        except Exception as e:
            error_msg = traceback.format_exc()
            logger.error(f"ATC Agent Error Details:\n{error_msg}")
            return "Flight 001, tower is reading you. Airspace clear. Maintain current heading."
