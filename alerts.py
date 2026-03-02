from gmail_auth import get_gmail_service
from email.mime.text import MIMEText
import base64

def send_weather_alert(event, analysis, prediction):

    service = get_gmail_service()

    message_text = f"""
Weather Update:

Temperature: {event['temperature']} °C
Wind Speed: {event['windspeed']} km/h

Risk Level: {analysis['risk']}
Prediction: {prediction['prediction']}
"""

    message = MIMEText(message_text)
    message['to'] = "shubharaj241@gmail.com"
    message['subject'] = "🌤 Autonomous Weather Update"

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    body = {'raw': raw_message}

    service.users().messages().send(userId="me", body=body).execute()

    print("Email sent via Gmail API")