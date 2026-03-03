import requests
import os
import json
from groq import Groq
from memory import store_event
from dotenv import load_dotenv

load_dotenv()

LAT = 10.99   # Tamil Nadu approx
LON = 78.00

def monitoring_agent():
    # Fetch current weather and daily precipitation probabilities
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current_weather=true&daily=precipitation_probability_max,precipitation_sum&timezone=auto"
    data = requests.get(url).json()
    
    weather = data['current_weather']
    daily = data.get('daily', {})
    
    # Get today's precipitation data
    rain_probability = daily.get('precipitation_probability_max', [0])[0]
    precipitation_mm = daily.get('precipitation_sum', [0.0])[0]
    
    event = {
        "temperature": weather['temperature'],
        "windspeed": weather['windspeed'],
        "rain_probability": rain_probability,
        "precipitation_mm": precipitation_mm
    }
    
    store_event(event)
    return event

def llm_reasoning_agent(event):
    """
    This is the true Agentic AI brain. It takes the raw event data,
    reasons about it using an LLM, and decides what actions to take.
    """
    try:
        api_key = os.environ.get("GROQ_API_KEY")
        model_name = os.environ.get("MODEL_NAME", "llama-3.1-8b-instant")
        
        if not api_key:
            print("WARNING: GROQ_API_KEY not found in environment variables. Falling back to default.")
            return {
                "risk": "API_KEY_MISSING",
                "rain_prediction": "Unable to predict without LLM.",
                "decisions": ["NO_ACTION"]
            }

        client = Groq(api_key=api_key)
        
        system_prompt = """You are an autonomous agricultural AI agent.
Your job is to read real-time weather data and make decisions for a farm.

Available decisions you can make (choose 0 or more):
- "COOLING_REQUIRED" (if temperature is high and heat stress is likely)
- "SEND_ALERT" (if conditions are dangerous)
- "SKIP_IRRIGATION" (if rain is highly likely or sufficient precipitation is expected)
- "IRRIGATION_NEEDED" (if it is dry and rain is unlikely)

You must output your response in valid JSON format exactly matching this structure:
{
  "risk": "A short description of heat/weather risk (e.g. HIGH_HEAT, NORMAL)",
  "rain_prediction": "A readable sentence about what farmers should do regarding rain/water.",
  "ai_insight": "A customized 2-5 sentence paragraph explicitly explaining WHY you as the AI made these specific observations and chosen actions based on the immediate weather data.",
  "decisions": ["LIST_OF_DECISIONS_FROM_AVAILABLE_LIST"]
}
Limit the 'risk' to one or two words.
Do NOT output any markdown blocks, only the raw JSON text.
"""

        user_prompt = f"Here is the current weather event data:\n{json.dumps(event)}"

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=256,
            response_format={"type": "json_object"}
        )
        
        result_content = response.choices[0].message.content
        result_json = json.loads(result_content)
        
        return result_json

    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return {
            "risk": "ERROR",
            "rain_prediction": "Error calling reasoning engine.",
            "decisions": ["NO_ACTION"]
        }