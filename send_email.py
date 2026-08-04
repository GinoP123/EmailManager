#!/Users/ginoprasad/miniconda3/bin/python3

import os
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sys


os.chdir(os.path.dirname(sys.argv[0]))

assert len(sys.argv) >= 4
subject = sys.argv[1]
content = sys.argv[2]
recipients = sys.argv[3:]


SCOPES = ['https://mail.google.com/']

creds = None
if os.path.exists('api_key/token.json'):
    creds = Credentials.from_authorized_user_file('api_key/token.json', SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('api_key/client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)

    with open('api_key/token.json', 'w') as token:
        token.write(creds.to_json())

service = build('gmail', 'v1', credentials=creds)


message = EmailMessage()
message.set_content(content, subtype='html')
message['To'] = ','.join(recipients)
message['Subject'] = subject

encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
create_message = {'raw': encoded_message}

send_result = service.users().messages().send(userId="me", body=create_message).execute()
print(f"Email sent successfully! Message ID: {send_result['id']}")



