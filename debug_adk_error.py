from google.genai import types
from google.adk import Agent, Runner
from google.adk.sessions import InMemorySessionService
from config import logger

agent = Agent(name="Test", model="gemini-2.5-flash", instruction="Test")
runner = Runner(agent=agent, app_name="test", session_service=InMemorySessionService(), auto_create_session=True)

events = runner.run(
    user_id="u",
    session_id="s",
    new_message=types.Content(role="user", parts=[types.Part.from_text(text="Say nothing.")])
)

for e in events:
    print(f"ERROR: {getattr(e, 'error_message', None)}")
