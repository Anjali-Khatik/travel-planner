# Purpose: Extract structured preferences from user input
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
import json
import re
load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",  # Groq model name
    temperature=0.2
)

prompt = ChatPromptTemplate.from_template("""
You are a travel assistant. Extract the following from this message:
- budget: low, medium, or high
- duration (in days)
- season: spring, summer, fall, winter
- interests (beach, romantic, adventure, culture, history, food, nature, relaxation)

Respond in JSON only.

User message: {input}
""")

def extract_preferences(state):
    user_input = state.history[-1]["message"]

    try:
        # LLM version (only if API is live)
        chain = prompt | llm
        response = chain.invoke({"input": user_input})
        print("LLM RAW OUTPUT:", response.content)
        def safe_json_parse(text):
            try:
                return json.loads(text)
            except:
                match = re.search(r"\{.*\}", text, re.DOTALL)
                if match:
                    return json.loads(match.group())
                raise

        state.preferences = safe_json_parse(response.content)
        # state.preferences = eval(response.content)
    except Exception as e:
        # Rule-based fallback
        print("[Fallback] LLM failed, using rule-based preference extraction.")
        user_input = user_input.lower()
        preferences = {}
        
        # 1. Budget
        if "low" in user_input: preferences["budget"] = "low"
        elif "medium" in user_input: preferences["budget"] = "medium"
        elif "high" in user_input: preferences["budget"] = "high"

        # 2. Season
        if "spring" in user_input: preferences["season"] = "spring"
        elif "summer" in user_input: preferences["season"] = "summer"
        elif "fall" in user_input or "autumn" in user_input: preferences["season"] = "fall"
        elif "winter" in user_input: preferences["season"] = "winter"

        # 3. Interests
        interests = [tag for tag in ["beach", "romantic", "adventure", "culture", "history", "food", "nature", "relaxation"] if tag in user_input]
        if interests: 
            preferences["interests"] = interests

        # 4. Duration(in days)
        for word in user_input.split():
            if word.isdigit():
                preferences["duration"] = int(word)
                break

        state.preferences = preferences

    return state
