import os
import base64
import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    cred_data_b64 = os.environ.get("GMAIL_CREDENTIALS", "")
    token_data_b64 = os.environ.get("GMAIL_TOKEN", "")
    
    # Fallback to reading .env file manually if env vars aren't loaded properly
    if not cred_data_b64 or not token_data_b64:
        try:
            with open('.env', 'r') as f:
                content = f.read()
            import re
            if not cred_data_b64:
                cred_match = re.search(r'GMAIL_CREDENTIALS=(.*?)(?:\n\n|\r?\n\r?\n|\Z)', content, re.DOTALL)
                if cred_match:
                    cred_data_b64 = cred_match.group(1).replace('\n', '').replace('\r', '')
            if not token_data_b64:
                token_match = re.search(r'GMAIL_TOKEN=(.*?)(?:\n\n|\r?\n\r?\n|\Z)', content, re.DOTALL)
                if token_match:
                    token_data_b64 = token_match.group(1).replace('\n', '').replace('\r', '')
        except FileNotFoundError:
            pass

    if not cred_data_b64 or not token_data_b64:
        print("Gmail tokens not found in environment.")
        return None

    try:
        # Decode the base64 tokens
        token_data_str = base64.b64decode(token_data_b64).decode('utf-8')
        token_info = json.loads(token_data_str)
        
        # Load credentials directly from dict (no file write)
        creds = Credentials.from_authorized_user_info(token_info, SCOPES)
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(f"Failed to initialize Gmail API service: {e}")
        return None