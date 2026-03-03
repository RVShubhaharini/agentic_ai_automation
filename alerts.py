import os
from gmail_auth import get_gmail_service
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import smtplib
from dotenv import load_dotenv

load_dotenv()

def send_via_gmail_api(message_text, subject, to_email):
    service = get_gmail_service()
    if not service:
        raise ValueError("Gmail API service could not be initialized.")

    message = MIMEText(message_text)
    message['to'] = to_email
    message['subject'] = subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {'raw': raw_message}

    service.users().messages().send(userId="me", body=body).execute()
    print("Email sent successfully via Gmail API (Tokens)")

def send_via_smtp(message_text, subject, to_email):
    sender = os.environ.get("EMAIL")
    password = os.environ.get("APP_PASSWORD")
    smtp_server = os.environ.get("EMAIL_SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("EMAIL_SMTP_PORT", 587))

    if not sender or not password:
        raise ValueError("SMTP credentials (EMAIL/APP_PASSWORD) not found in environment.")

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message_text, 'plain'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()
    print("Email sent successfully via SMTP (Mail Credentials)")

def send_weather_alert(event, analysis, prediction, actions):
    subject = "🌤 Autonomous Farm & Weather Update"
    to_email = os.environ.get("TO_EMAIL", "shubhaharinirv@gmail.com")

    message_text = f"""
🌤 Autonomous Farm & Weather Update

Data Source: Open-Meteo Forecast API
(We use real-time meteorological models to predict precipitation probabilities and sums for your exact location).

Current Conditions:
- Temperature: {event.get('temperature', 'N/A')} °C
- Wind Speed: {event.get('windspeed', 'N/A')} km/h

Forecast (Today):
- Rain Probability: {event.get('rain_probability', 0)}%
- Expected Precipitation: {event.get('precipitation_mm', 0.0)} mm

Assessments:
- Heat Risk: {analysis.get('risk', 'N/A')}
- Rain Prediction: {prediction.get('rain_prediction', 'Data unavailable')}

🧠 AI Insights (Groq llama-3.1-8b):
{prediction.get('ai_insight', 'No explicit AI reasoning provided.')}

Automated Actions Taken:
- {chr(10).join(['- ' + action for action in actions]) if actions else 'None'}
"""

    # Print log that we are attempting to send mail
    print(f"Attempting to send email alert to {to_email}...")

    # First attempt: Gmail API via tokens
    try:
        send_via_gmail_api(message_text, subject, to_email)
        return
    except Exception as api_err:
        print(f"Gmail API method failed: {api_err}. Falling back to SMTP...")

    # Second attempt: SMTP using mail credentials (app password)
    try:
        send_via_smtp(message_text, subject, to_email)
    except Exception as smtp_err:
        print(f"SMTP method also failed: {smtp_err}.")
        print("Could not send email alert.")