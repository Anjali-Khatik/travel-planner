# Purpose: Load weather data and provide forecasts for destinations

import json

def load_weather_data(filepath):

    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def get_weather_forecast(city, days, weather_data=None):
    
    if weather_data is None:
        weather_data = load_weather_data("data/weather_data.json")

    forecast = weather_data.get(city)
    if not forecast:
        return ["Sunny"] * days  # Default weather

    # Return as many days as requested, looping if not enough data
    result = []
    for i in range(days):
        result.append(forecast[i % len(forecast)])
    return result
