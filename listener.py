#!/Users/ginoprasad/miniconda3/envs/google-api/bin/python3

import os, glob
import sys
import settings
import json
import concurrent.futures
from google.cloud import pubsub_v1
import google.auth
import subprocess as sp
import time
import base64
import re

cmd = "ps -Ao pid,args"
curr_ids = set(map(str, (os.getpid(), os.getppid())))

siblings = [None]
num_procs_end = 0
while siblings and num_procs_end < settings.max_procs_end:
    procs = sp.getoutput(cmd).strip().split('\n')
    is_sibling = lambda proc: proc.strip().split(' ')[0] not in curr_ids
    siblings = [proc for proc in procs if sys.argv[0] in proc and is_sibling(proc)]

    if siblings:
        sibling_id = siblings[0].strip().split(' ')[0]
        print(f"\nDuplicate Process Found:\n\t{siblings[0]}\n\n")
        sp.run(f"kill -9 {sibling_id}", shell=True)
        num_procs_end += 1
        time.sleep(5)
        

os.chdir(os.path.dirname(sys.argv[0]))
import utils


credentials, default_project = google.auth.default(
    quota_project_id=settings.project_id
)

subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
subscription_path = subscriber.subscription_path(settings.project_id, settings.subscription_id)


def extract_text(payload):
    if 'parts' in payload:
        return ''.join(map(extract_text, payload['parts']))
    elif payload.get('mimeType') == 'text/plain':
        data = payload.get('body', {}).get('data', '')
        if data:
            return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    return ''


def callback(message):
    message.ack()
    list_res = utils.service.users().messages().list(userId='me', q='in:inbox', maxResults=1).execute()
    messages = list_res.get('messages', [])
    eid = messages[0]['id']

    if eid == utils.get_last_email_id():
        return

    utils.update_last_email_id(eid)

    msg = utils.service.users().messages().get(
        userId='me', id=eid, format='full'
    ).execute()

    email_from = ','.join([x['value'] for x in msg['payload']['headers'] if x['name'] == 'From'])

    labels = msg.get('labelIds', [])
    if 'INBOX' in labels and 'SENT' not in labels and 'info@account.netflix.com' in email_from:
        payload = extract_text(msg['payload'])
        
        code = re.search(r'(?<=Get Code\r\n\[)https://.*?(?=[ \]])', payload)
        if code is None:
            code = re.search(r'(?<=Enter this code to sign in\r\n\r\n)[0-9][0-9][0-9][0-9]', payload)
        if code is None:
            with open(settings.payload_path, 'w') as outfile:
                outfile.write(payload)
        code = code.group()

        message = f'Netflix Code: {code}'
        assert len(set("\n'\"") - set(message)) == 3

        cmd = f"'{settings.ttab_path}' '{settings.send_text_path}' '{settings.group_chat_id}' '{message}'"
        sp.run(cmd, shell=True)


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

try:
    streaming_pull_future.result(timeout=settings.TIMEOUT)
except concurrent.futures.TimeoutError:
    streaming_pull_future.cancel()
    print(f"{settings.TIMEOUT} second window finished. Exiting gracefully.")




