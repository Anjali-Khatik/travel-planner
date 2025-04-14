
from random import sample
from agent.tools.weather_tool import get_weather_forecast

def create_itinerary(state):
    
    if not state.destinations:
        state.itinerary = {"error": "No destinations found."}
        return state

    destination = state.destinations[0]  # select top match
    city = destination["name"]
    days = state.preferences.get("duration", 3)
    weather = get_weather_forecast(city, days)

    # Define a pool of activity templates based on possible interests
    activity_bank = {
        "romantic": ["Sunset dinner", "Stroll by the lake", "Couples' spa"],
        "beach": ["Beach volleyball", "Snorkeling", "Relax on the beach"],
        "adventure": ["Zip-lining", "Hiking", "River rafting"],
        "culture": ["Visit a museum", "Cultural performance", "Local craft workshop"],
        "history": ["Tour a historical site", "Visit ancient ruins", "Heritage walk"],
        "food": ["Street food tour", "Cooking class", "Try a regional specialty"],
        "nature": ["Nature walk", "Bird watching", "Botanical garden tour"],
        "relaxation": ["Spa treatment", "Yoga session", "Poolside chill"]
    }

    user_tags = state.preferences.get("interests", [])
    plan = []

    for i in range(days):
        activities = []
        # For each day, pick 2 random activities from relevant tags
        for tag in user_tags:
            if tag in activity_bank:
                activities.extend(sample(activity_bank[tag], min(1, len(activity_bank[tag]))))
        # Fallback generic activity if user has no tags
        if not activities:
            activities = [f"Explore {city}", "Try local food", "Visit scenic spots"]
        else:
            activities = sample(activities, min(3, len(activities)))  # Limit to 3 per day

        plan.append({
            "day": i + 1,
            "activities": activities,
            "weather": weather[i]
        })

    state.itinerary = {
        "destination": city,
        "days": plan
    }
    return state