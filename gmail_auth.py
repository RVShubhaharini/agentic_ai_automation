import os
import base64
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    # os.getenv doesn't reliably handle multiline variables without quotes
    # So we'll parse the .env file directly to get the full base64 strings
    cred_data_b64 = ""
    token_data_b64 = ""
    
    with open('.env', 'r') as f:
        content = f.read()
        
    import re
    cred_match = re.search(r'GMAIL_CREDENTIALS=(.*?)(?:\n\n|\Z)', content, re.DOTALL)
    if cred_match:
        cred_data_b64 = cred_match.group(1).replace('\n', '')
        
    token_match = re.search(r'GMAIL_TOKEN=(.*?)(?:\n\n|\Z)', content, re.DOTALL)
    if token_match:
        token_data_b64 = token_match.group(1).replace('\n', '')

    cred_data = base64.b64decode(cred_data_b64).decode()
    token_data = base64.b64decode(token_data_b64).decode()

    with open("credentials.json", "w") as f:
        f.write(cred_data)

    with open("token.json", "w") as f:
        f.write(token_data)

    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('gmail', 'v1', credentials=creds)

    return service