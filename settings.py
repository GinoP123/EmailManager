import datetime


SCOPES = ['https://mail.google.com/']

token_file = 'api_key/token.json'
client_file = 'api_key/client_secret.json'

last_email_cache_file = 'cron_log/last_email.txt'

project_id = "mail-service-504402"
subscription_id = "gmail-notifications-sub"

send_text_path = "/Users/ginoprasad/Scripts/BlueBubblesHandler/send_message.py"
group_chat_id = '+;chat92082781927135072'
payload_path = 'payload.txt'

TIMEOUT = int(datetime.timedelta(hours=1).total_seconds())


email_list = [
	'ginoprasad@gmail.com',
    'anyaprasad24@gmail.com',
	'neilprasad4@gmail.com',
	'caroline.prasad@iac.com',
	'jakeprasad@gmail.com'
]

ttab_path = "/opt/homebrew/bin/ttab"

max_procs_end = 5
