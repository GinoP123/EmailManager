import os
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sys
import json
import concurrent.futures
from google.cloud import pubsub_v1
import settings



creds = None
if os.path.exists(settings.token_file):
    creds = Credentials.from_authorized_user_file(settings.token_file, settings.SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(settings.client_file, settings.SCOPES)
        creds = flow.run_local_server(port=0)

    with open(settings.token_file, 'w') as token:
        token.write(creds.to_json())

service = build('gmail', 'v1', credentials=creds)



def stop_watch(service):
    service.users().stop(userId='me').execute()


def start_watch(service):
    request_body = {
        'labelIds': ['INBOX'],
        'topicName': f'projects/{settings.project_id}/topics/gmail-notifications',
        'labelFilterBehavior': 'INCLUDE'
    }
    return service.users().watch(userId='me', body=request_body).execute()



