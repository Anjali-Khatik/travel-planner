# Purpose: Run a sample flow using your agent interactively

from agent.graph import build_travel_graph
from agent.state import AgentState

def run_agent():
    graph = build_travel_graph()

    # Initialize state on first input
    state = AgentState()
    state.history=[]
    printed_itinerary = True  # control flag
    

    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        state.history.append({"role": "user", "message": user_input})
        

        # follow-up vs. new plan
        last_msg = state.history[-1]["message"].lower()
        followup_keywords = [
            "shorten", "longer", "change", "update", "make it", "reduce",
            "can you", "instead", "add", "remove"
        ]

        if len(state.history) > 1 and any(kw in last_msg for kw in followup_keywords):
            state.is_followup = True
        else:
            state.is_followup = False

        
        # Stream the graph execution (simulate assistant thinking)
        for output in graph.stream(state):
            for step, value in output.items():
                if value['itinerary'] :
                    if value['itinerary'] and printed_itinerary:
                        print("--- Itinerary Created ---")
                        print(value["itinerary"])
                        printed_itinerary=False
                    elif value["followup_response"]:
                        print("--- Based on Follow-Up itinerary is updated ---")
                        print(value["itinerary"])

if __name__ == "__main__":
    run_agent()