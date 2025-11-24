import os
import base64
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials

# Gmail API Scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Get absolute paths for credentials and token
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # users folder
CREDENTIALS_FILE = os.path.join(BASE_DIR, 'credentials.json')
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')

# Authenticate and get credentials (OAuth2)
def authenticate():
    creds = None
    # Load existing token if it exists
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # If there are no valid credentials, log in and save new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds

# Send an email using Gmail API
def send_email(sender, to, subject, body):
    creds = authenticate()  # authenticate and get creds

    # Build the Gmail API service
    service = build('gmail', 'v1', credentials=creds)

    # Create the email message
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Send the email via Gmail API
    sent_message = service.users().messages().send(
        userId="me",
        body={'raw': raw_message}
    ).execute()

    print(f'Email sent! Message ID: {sent_message["id"]}')

send_email("lrrawool2503@gmail.com", "lalitrawool25@gmail.com", "subject", "body")