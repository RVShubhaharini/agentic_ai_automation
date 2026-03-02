import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()

EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

def send_weather_alert(event, analysis, prediction):

    subject = "🌤 Autonomous Weather Update"
    
    body = f"""
    Weather Update:

    Temperature: {event['temperature']} °C
    Wind Speed: {event['windspeed']} km/h

    Risk Level: {analysis['risk']}
    Prediction: {prediction['prediction']}
    """

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL
    msg['To'] = TO_EMAIL

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()