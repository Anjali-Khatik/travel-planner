import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.state import AgentState
from agent.nodes.preference_extractor import extract_preferences
from agent.nodes.destination_finder import find_destinations
from agent.nodes.itinerary_creator import create_itinerary
from agent.nodes.followup_handler import handle_followup
from agent.graph import build_travel_graph

# Test 1: Check if preferences are extracted correctly
def test_preference_extraction():
    state = AgentState()
    state.history = [{"role": "user", "message": "I want a beach vacation for 5 days in summer with a medium budget"}]
    new_state = extract_preferences(state)
    
    assert new_state.preferences["budget"] == "medium"
    assert new_state.preferences["duration"] == 5
    assert "beach" in new_state.preferences["interests"]
    assert new_state.preferences["season"] == "summer"

# Test 2: Check if destination filtering works
def test_destination_filtering():
    state = AgentState()
    state.preferences = {
        "budget": "medium",
        "duration": 5,
        "interests": ["beach", "romantic"],
        "season": "summer"
    }
    new_state = find_destinations(state)
    
    assert len(new_state.destinations) > 0
    assert any("beach" in d["tags"] for d in new_state.destinations)

# Test 3: Run the full graph flow (input → itinerary)
def test_end_to_end_flow():
    graph = build_travel_graph()
    state = AgentState()
    state.history = [{"role": "user", "message": "Plan a food and culture trip for 4 days in fall with a low budget"}]
    state.is_followup = False
    
    final_state = graph.invoke(state)
    assert "itinerary" in final_state
    assert "destination" in final_state["itinerary"]
    assert len(final_state["itinerary"]["days"]) == 4

# Test 4: Simulate a follow-up update
def test_followup_handling():
    state = AgentState()
    state.history = [{"role": "user", "message": "Can you reduce the trip to 3 days?"}]
    state.preferences = {
        "budget": "medium",
        "duration": 5,
        "interests": ["culture"],
        "season": "winter"
    }
    state.is_followup = True

    updated_state = handle_followup(state)
    assert updated_state.preferences["duration"] == 3
    assert hasattr(updated_state, "followup_response")
    assert isinstance(updated_state.followup_response, str)

