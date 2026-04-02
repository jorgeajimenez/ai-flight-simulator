from services.control_tower import tower_runner
from google.genai import types

events = tower_runner.run(
    user_id="pilot_1",
    session_id="flight_debug",
    new_message=types.Content(
        role="user", 
        parts=[types.Part.from_text(text="Control Tower, this is Flight 001 Copilot over Paris. Requesting time and local factoid.")]
    )
)

final_text = ""
for e in events:
    print(f"EVENT TYPE: {type(e)}")
    print(f"IS_FINAL: {getattr(e, 'is_final_response', False)}")
    if e.content and e.content.parts:
        print(f"PARTS: {e.content.parts}")
        for part in e.content.parts:
            if part.text:
                final_text += part.text

print(f"FINAL TEXT: '{final_text}'")
