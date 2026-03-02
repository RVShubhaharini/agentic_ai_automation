import requests
from memory import store_event

LAT = 10.99   # Tamil Nadu approx
LON = 78.00

def monitoring_agent():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current_weather=true"
    data = requests.get(url).json()
    
    weather = data['current_weather']
    
    event = {
        "temperature": weather['temperature'],
        "windspeed": weather['windspeed']
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
        
    return {"prediction": prediction}