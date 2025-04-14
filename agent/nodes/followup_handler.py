def handle_followup(state):
    user_message = state.history[-1]["message"].lower()

    # Modify preferences
    if "shorten" in user_message or "3 days" in user_message:
        state.preferences["duration"] = 3
    elif "5 days" in user_message:
        state.preferences["duration"] = 5

    if "adventure" in user_message and "adventure" not in state.preferences.get("interests", []):
        state.preferences.setdefault("interests", []).append("adventure")

    if "low budget" in user_message or "cheaper" in user_message:
        state.preferences["budget"] = "low"

    # Reset old results to re-trigger the pipeline
    state.destinations = []
    state.itinerary = {}
    state.followup_response = "Preferences updated based on your follow-up. Replanning your itinerary..."

    state.is_followup = False

    return state
