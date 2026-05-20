#!/bin/bash
# Script to populate the GitHub repository with the codelab tickets using the 'gh' CLI

if ! command -v gh &> /dev/null
then
    echo "GitHub CLI (gh) could not be found. Please install it to create issues."
    exit
fi

echo "Creating GitHub Issues for AI Flight Simulator..."

gh issue create --title "Ticket #1: Reverse Geocoding Utility" --body-file tickets/TICKET-1.md --label "enhancement"
gh issue create --title "Ticket #2: Procedural Biome Generation" --body-file tickets/TICKET-2.md --label "enhancement"
gh issue create --title "Ticket #3: The ADK Control Tower" --body-file tickets/TICKET-3.md --label "enhancement"
gh issue create --title "Ticket #4: The Copilot Agent" --body-file tickets/TICKET-4.md --label "enhancement"

echo "Done! Issues have been populated."
