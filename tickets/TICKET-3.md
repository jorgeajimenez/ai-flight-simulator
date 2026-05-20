# Ticket #3: The ADK Control Tower

**Status:** TODO
**Module:** `services/control_tower.py`

## Background
The flight simulator needs an autonomous Agent that can act as a Control Tower. Instead of just answering text prompts, this agent must be able to use external Tools (functions) to fetch live operational data (like local time) before responding to the pilot.

## Engineering Specification
Implement the `control_tower_agent` and `tower_runner` using the Google Agent Development Kit (ADK).

### Requirements:
1. **The Tool:** 
   - Create a simple Python function `get_local_time(city_name: str) -> str` that returns `"9:00 AM Local Time"` (mocked for the codelab).
2. **The Agent:**
   - Instantiate an ADK `Agent`.
   - Name it `"ControlTower"`.
   - Assign the model `"gemini-2.5-flash"`.
   - Provide strict instructions to ALWAYS use the `get_local_time` tool when hailed, and to respond concisely (under 3 sentences) with the time and a factoid.
   - Bind the `get_local_time` function to the agent's tools array.
3. **The Runner:**
   - Instantiate an `InMemorySessionService`.
   - Wrap the Agent in an ADK `Runner` to handle conversational memory and automated tool execution.

### Constraints
- Must use the official `google.adk` library.