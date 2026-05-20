# Ticket #4: The Copilot Agent

**Status:** TODO
**Module:** `services/control_tower.py`

## Background
With the ADK Control Tower running in the background, we need a frontend-facing interface (The Copilot) that takes the pilot's raw request and formally orchestrates the Agent-to-Agent (A2A) communication loop.

## Engineering Specification
Implement the `request_airspace_update(city_name: str) -> str` method within the `CopilotAgent` class.

### Requirements:
1. **Runner Execution:**
   - Trigger the `tower_runner.run()` method.
   - Pass in a `new_message` constructed from `types.Content` requesting an update for the specific `city_name` (e.g., "Requesting update for Paris").
2. **Event Parsing:**
   - Iterate over the events returned by the Runner.
   - Concatenate all text parts from the `event.content.parts`.
3. **Return Format:**
   - Return the final, synthesized string representing the Control Tower's briefing.
   - If the transmission is empty or fails, return a fallback string: `"Captain, we are unable to reach the Control Tower..."`

### Constraints
- Handle potential ADK execution errors gracefully to prevent 500 server errors on the `/locate` endpoint.