# Purpose: Load and filter destinations from destinations.json
import json

def load_destinations(filepath):
    with open(filepath, "r") as file:
        destinations = json.load(file)
    return destinations

def filtered_destination(preferences):
    """
    preference would be type Dict
    destinations would be list of dict
    
    """
    filtered = []
    destinations = load_destinations("data/destinations.json")

    for destination in destinations:

        # 1. Budget Check
        if preferences.get("budget"):
            if destination["budget_level"] != preferences.get("budget"): 
                continue

        # 2. Interests
        if preferences.get("interests"):
            if not any(tag in destination["tags"] for tag in preferences.get("interests")):
                continue

        # 3. Duration
        if preferences.get("duration"):
            min_dur, max_dur = destination.get("ideal_duration", [0, 999])
            if not (min_dur <= preferences.get("duration", 0) <= max_dur):
                continue

        # 4. Season check
        if preferences.get("season"):
            if preferences.get("season")  not in destination.get("best_seasons", []):
                continue

        # If all checks passed
        filtered.append(destination)

    return filtered