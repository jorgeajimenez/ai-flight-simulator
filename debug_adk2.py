from services.control_tower import CopilotAgent

print(CopilotAgent.request_airspace_update("London"))
print(CopilotAgent.request_airspace_update("Berlin"))
