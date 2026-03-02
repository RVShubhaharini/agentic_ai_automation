import requests
from memory import store_event

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


def analysis_agent(event):
    risk = "NORMAL"
    
    if event['temperature'] > 35:
        risk = "HIGH_HEAT"
        
    return {"risk": risk}


def prediction_agent(event):
    prediction = "SAFE"
    
    if event['temperature'] > 37:
        prediction = "HEAT_STRESS_RISK"
        
    # Irrigation focus: predict if rain is coming today based on Open-Meteo precipitation probability
    rain_prediction = "Low chance of rain. Irrigation is needed."
    if event['rain_probability'] > 60 or event['precipitation_mm'] > 2.0:
        rain_prediction = f"High chance of rain ({event['rain_probability']}%). Farmers need not water plants."
    elif event['rain_probability'] > 30 or event['precipitation_mm'] > 0.5:
        rain_prediction = f"Moderate chance of rain ({event['rain_probability']}%). Farmers can reduce or skip watering."
        
    return {
        "prediction": prediction,
        "rain_prediction": rain_prediction
    }