#!/Users/ginoprasad/miniconda3/envs/google-api/bin/python3


import os, glob
import sys
os.chdir(os.path.dirname(sys.argv[0]))

import utils
import settings
from email.message import EmailMessage
import base64

if len(sys.argv) == 2:
    msg_id = sys.argv[1]
else:
    list_res = utils.service.users().messages().list(userId='me', q='in:inbox', maxResults=1).execute()
    messages = list_res.get('messages', [])
    msg_id = messages[0]['id']

original_msg = utils.service.users().messages().get(userId='me', id=msg_id, format='full').execute()

headers = original_msg.get('payload', {}).get('headers', [])
subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
snippet = original_msg.get('snippet', '')


def extract_body(payload):
    if 'parts' in payload:
        for part in payload['parts']:
            if part.get('mimeType') == 'text/plain' and 'data' in part.get('body', {}):
                return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
    elif 'body' in payload and 'data' in payload['body']:
        return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
    return snippet


body_text = extract_body(original_msg.get('payload', {}))

new_message = EmailMessage()
new_message['To'] = ','.join(settings.email_list)
new_message['Subject'] = subject
new_message.set_content(body_text)

raw_bytes = new_message.as_bytes()
encoded_message = base64.urlsafe_b64encode(raw_bytes).decode('utf-8')

sent_message = utils.service.users().messages().send(
    userId='me',
    body={'raw': encoded_message}
).execute()


print(f"Successfully sent message ID: {sent_message['id']}")


