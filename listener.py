#!/Users/ginoprasad/miniconda3/envs/google-api/bin/python3

import os, glob
import sys
import settings
import datetime
import json
import concurrent.futures
from google.cloud import pubsub_v1
import google.auth

os.chdir(os.path.dirname(sys.argv[0]))
import utils


credentials, default_project = google.auth.default(
    quota_project_id=settings.project_id
)

subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
subscription_path = subscriber.subscription_path(settings.project_id, settings.subscription_id)

def callback(message):
    data = json.loads(message.data.decode('utf-8'))
    datetime_string = '_'.join(str(datetime.datetime.now()).split(' '))
    with open(f"email_log/{datetime_string}", 'w') as outfile:
        outfile.write(f"Latest History ID: {data.get('historyId')}\n")
        outfile.write(f"Payload: {data}")
    message.ack()


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

try:
    streaming_pull_future.result(timeout=settings.TIMEOUT)
except concurrent.futures.TimeoutError:
    streaming_pull_future.cancel()
    print(f"{settings.TIMEOUT} second window finished. Exiting gracefully.")




