import datetime

log_path = "cron_log/log.txt"
create_event_path = "/Users/ginoprasad/Scripts/ScheduleManager/create_event.py"
logging_emails = ["giprasad@ucsd.edu"]
error_message = "EmailManager Ran Into Error!!!"

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



regex_include = [
    r'(?<=Get Code\r\n\[)https://.*?(?=[ \]])',
    r'(?<=Enter this code to sign in\r\n\r\n)[0-9][0-9][0-9][0-9]',
    r'(?<=Yes, This Was Me\r\n\[)https://.*?(?=[\]])',
]

regex_exclude = [
    'Please review who’s using your Netflix account',
    'We’ve updated your account with your new payment info',
    'Your Netflix Household has been confirmed',
    'we’re updating our prices',
    "Here's a quick summary of key updates to reflect our new features and services",
    'We recently announced that',
    'Your 4K upgrade ends soon'
]

emails_watch = [
    'info@account.netflix.com'
]



