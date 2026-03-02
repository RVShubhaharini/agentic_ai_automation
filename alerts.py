from gmail_auth import get_gmail_service
from email.mime.text import MIMEText
import base64

def send_weather_alert(event, analysis, prediction, actions):

    service = get_gmail_service()

    message_text = f"""
🌤 Autonomous Farm & Weather Update

Data Source: Open-Meteo Forecast API
(We use real-time meteorological models to predict precipitation probabilities and sums for your exact location).

Current Conditions:
- Temperature: {event['temperature']} °C
- Wind Speed: {event['windspeed']} km/h

Forecast (Today):
- Rain Probability: {event.get('rain_probability', 0)}%
- Expected Precipitation: {event.get('precipitation_mm', 0.0)} mm

Assessments:
- Heat Risk: {analysis['risk']}
- Rain Prediction: {prediction.get('rain_prediction', 'Data unavailable')}

Automated Actions Taken:
- {chr(10).join(['- ' + action for action in actions])}
"""

    message = MIMEText(message_text)
    message['to'] = "shubharaj241@gmail.com"
    message['subject'] = "🌤 Autonomous Farm & Weather Update"

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    body = {'raw': raw_message}

    service.users().messages().send(userId="me", body=body).execute()

    print("Email sent via Gmail API")