import requests
import os
import json
from groq import Groq
from memory import store_event, get_historical_events
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
    rain_probability = daily.get('precipitation_probability_max', [0, 0])[0]
    precipitation_mm = daily.get('precipitation_sum', [0.0, 0.0])[0]
    
    # Get tomorrow's precipitation data
    tomorrow_rain_probability = daily.get('precipitation_probability_max', [0, 0])[1] if len(daily.get('precipitation_probability_max', [])) > 1 else 0
    tomorrow_precipitation_mm = daily.get('precipitation_sum', [0.0, 0.0])[1] if len(daily.get('precipitation_sum', [])) > 1 else 0.0
    
    event = {
        "temperature": weather['temperature'],
        "windspeed": weather['windspeed'],
        "rain_probability": rain_probability,
        "precipitation_mm": precipitation_mm,
        "tomorrow_rain_probability": tomorrow_rain_probability,
        "tomorrow_precipitation_mm": tomorrow_precipitation_mm
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
Your job is to read real-time weather data, including the forecast for tomorrow, and the history of recent weather events to make decisions for a farm.
Use the provided history of past events along with the current weather event to determine the trend and predict if rain will come in the future. Explain how the data from the past (like yesterday) informs today's prediction.
IMPORTANT INSTRUCTION 1: Analyze the past 3 records. 
- If they show high temperatures, state those temperatures and recommend the farmer to "do irrigation if needed".
- If they show low temperatures AND there was rain in the past records, state that they had low temperature and rain, and recommend "if wetness remains don't do irrigation, else do it".
IMPORTANT INSTRUCTION 2: Analyze tomorrow's forecast (provided as `tomorrow_rain_probability` and `tomorrow_precipitation_mm`). Provide a `future_prediction` indicating if it will rain tomorrow, and a `future_recommendation` advising the farmers on how to plan their agricultural activities today in advance of tomorrow's weather.

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
  "email_recommendation": "The requested historical recommendation sentence based on the last 3 records regarding irrigation and temperature.",
  "future_prediction": "What the weather will look like tomorrow based on the forecast data.",
  "future_recommendation": "Advance planning recommendation for the farmer based on tomorrow's prediction.",
  "decisions": ["LIST_OF_DECISIONS_FROM_AVAILABLE_LIST"]
}
Limit the 'risk' to one or two words.
Do NOT output any markdown blocks, only the raw JSON text.
"""

        history = get_historical_events(5)
        user_prompt = f"Here is the history of recent past weather events:\n{json.dumps(history, indent=2)}\n\nHere is the current weather event data:\n{json.dumps(event, indent=2)}"

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
            "email_recommendation": "No recommendation (Error)",
            "future_prediction": "Error calling reasoning engine.",
            "future_recommendation": "No recommendation (Error)",
            "decisions": ["NO_ACTION"]
        }