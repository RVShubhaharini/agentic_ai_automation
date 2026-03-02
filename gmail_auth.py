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

    cred_data = base64.b64decode(os.getenv("GMAIL_CREDENTIALS")).decode()
    token_data = base64.b64decode(os.getenv("GMAIL_TOKEN")).decode()

    with open("credentials.json", "w") as f:
        f.write(cred_data)

    with open("token.json", "w") as f:
        f.write(token_data)

    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('gmail', 'v1', credentials=creds)

    return service