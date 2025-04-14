# Travel Planner AI Agent 

This project implements an intelligent travel planner using **LangGraph**, **LangChain**, and **OpenAI's API**. The agent extracts user preferences, suggests destinations, and generates personalized itineraries through a multi-agent graph.

---

## Project Structure

```python
travel_planner/
├── agent/              # LangGraph setup (nodes and edges)
│   └── graph.py
├── config.py           # Loads API keys securely from .env
├── data/               # Mock datasets for destinations and weather
│   ├── destinations.json
│   └── weather_mock.json
├── main.py             # Interactive agent interface
├── nodes/              # LangGraph node functions
│   ├── preference_extractor.py
│   ├── destination_finder.py
│   ├── itinerary_creator.py
│   └── followup_handler.py
├── tools/              # Utility tools used by nodes
│   ├── destination_tool.py
│   └── weather_tool.py
├── tests/              # Unit tests
│   └── test_agent.py
├── .env                # Secret API key storage (not committed)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Features
+ Extracts preferences using LLM or rule-based fallback

+ Filters destinations by budget, duration, interests, and season

+ Generates a multi-day itinerary with weather info

+ Supports dynamic follow-up adjustments

+ Comes with a full suite of test cases

## LangGraph Flow

**Preference Extraction**: Extracts user preferences (budget, duration, season, interests)

**Destination Finder**: Filters matching locations from destinations.json

**Itinerary Creator**: Generates a daily itinerary with weather from weather_mock.json

**Follow-Up Handler**: Listens to feedback (e.g., "change to 3 days") and loops back

**Full flow is defined in agent/graph.py.**

## Environment Setup

### 1. Clone and Create Environment
```
cd travel_planner
python -m venv .venv
source .venv/bin/activate
```
### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Add .env File
```
OPENAI_API_KEY=your-openai-key-here
```
## How to Run It

### Interactive Mode
```
python -m main
```
### You can now chat with the AI:
```
User: I want a romantic beach trip for 5 days in summer with a medium budget
```
### Run Tests
```
pytest tests/test_agent.py
```

## Data Used

```destinations.json```

+ Each destination has:
  name, country, tags, budget_level, ideal_duration, best_seasons

```weather_mock.json```


+ Daily weather for all days for each city

+ Used to simulate a weather tool

## LLM Integration

The extract_preferences node uses:

+ OpenAI (ChatGPT-4o) via ChatOpenAI

+ A clean structured prompt with fallback to rule-based logic

+ Safe parsing using eval wrapped in try/except

*If quota is exhausted, fallback logic ensures continuity.*

## Test Coverage

+ ```test_preference_extraction```

+ ```test_destination_filtering```

+ ```test_end_to_end_flow```

+ ```test_followup_handling```

**Ensures the agent is reliable and maintainable**

## Future Improvements

+ Use real-time weather APIs

+ Add destination images or maps

+ Deploy as a web app using FastAPI + React

+ Add memory or user profile support


