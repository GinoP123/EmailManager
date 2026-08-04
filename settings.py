import datetime


SCOPES = ['https://mail.google.com/']

token_file = 'api_key/token.json'
client_file = 'api_key/client_secret.json'


project_id = "mail-service-504402"
subscription_id = "gmail-notifications-sub"

TIMEOUT = int(datetime.timedelta(hours=1).total_seconds())

