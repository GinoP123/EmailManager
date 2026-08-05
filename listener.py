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

def callback(message):
    message.ack()
    data = json.loads(message.data.decode('utf-8'))

    res = utils.service.users().history().list(
        userId='me', startHistoryId=data['historyId'], historyTypes=['messageAdded']
    ).execute()

    record = res['history'][0]['messagesAdded'][0]['message']
    if 'SENT' in record['labelIds'] or 'INBOX' not in record['labelIds']:
        continue

    output = sp.run(f"{settings.ttab_path} '{os.getcwd()}/forward_email.py; exit'", shell=True, capture_output=True).stdout.decode()
    print(output)


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

try:
    streaming_pull_future.result(timeout=settings.TIMEOUT)
except concurrent.futures.TimeoutError:
    streaming_pull_future.cancel()
    print(f"{settings.TIMEOUT} second window finished. Exiting gracefully.")




