from google.genai import types
from google.adk import Agent, Runner
from google.adk.sessions import InMemorySessionService
from config import logger

# TODO: [TICKET 3] Implement the ADK Control Tower Agent and Tool

class CopilotAgent:
    @staticmethod
    def request_airspace_update(city_name: str) -> str:
        # TODO: [TICKET 4] Implement the Copilot Agent to invoke the ADK Runner
        return f"Captain, we are currently holding pattern over {city_name}."
