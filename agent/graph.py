# Purpose: Wire together nodes into a LangGraph workflow

from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes.preference_extractor import extract_preferences
from agent.nodes.destination_finder import find_destinations
from agent.nodes.itinerary_creator import create_itinerary
from agent.nodes.followup_handler import handle_followup
from IPython.display import Image

def build_travel_graph():
    builder = StateGraph(AgentState)

    # Add nodes to graph
    builder.add_node("extract_preferences", extract_preferences)
    builder.add_node("find_destinations", find_destinations)
    builder.add_node("create_itinerary", create_itinerary)
    builder.add_node("handle_followup", handle_followup)

    # Add linear flow
    builder.set_entry_point("extract_preferences")
    builder.add_edge("extract_preferences", "find_destinations")
    builder.add_edge("find_destinations", "create_itinerary")

    # Conditional edge from itinerary to either END or handle_followup
    def route_after_itinerary(state: AgentState):
        return "handle_followup" if state.is_followup else END

    builder.add_conditional_edges("create_itinerary", route_after_itinerary)
    builder.add_edge("handle_followup", "find_destinations")  # reloop after follow-up


    return builder.compile()
