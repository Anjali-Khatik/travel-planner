# Purpose: Find destinations matching user preferences

from agent.tools.destination_tool import load_destinations, filtered_destination

def find_destinations(state):
    matches = filtered_destination(state.preferences)
    state.destinations = matches
    return state