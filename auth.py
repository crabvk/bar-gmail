#!/usr/bin/env python

from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import argparse

SCOPE = 'https://www.googleapis.com/auth/gmail.labels'
DIR = Path(__file__).resolve().parent
CLIENT_SECRETS_PATH = Path(DIR, 'client_secrets.json')
CREDENTIALS_PATH = Path(DIR, 'credentials.json')

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--addaccount", action='store_true')
parser.add_argument("-c", "--color", default= "#e06c75")
args = parser.parse_args()

credentials = {
    "count" : 0,
    "creds" : [],
}

def add_cred():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_PATH, scopes=[SCOPE])
    creds = flow.run_console()
    credentials["count"] += 1
    credentials["creds"].append( { "color": args.color, "cred" : json.loads(creds.to_json()) } )


if Path(CREDENTIALS_PATH).is_file():
    with open(CREDENTIALS_PATH, 'r') as f:
            credentials = json.load(f)
    if args.addaccount:
        add_cred()
    else:
        #check all credentials for expired
        refreshed = False
        for i in range(0, credentials["count"]):
            c = credentials["creds"][i]["cred"]
            creds= Credentials.from_authorized_user_info(c)
            if creds.expired and creds.refresh_token:
                refreshed = True
                creds.refresh(Request())
        if refreshed:
            print('Credentials looks ok, try to remove credentials.json if something doesn\'t work')
            exit()
else:
    add_cred()

# Save credentials
with open(CREDENTIALS_PATH, 'w') as creds_file:
    json.dump(credentials, creds_file)
print('Credentials successfully refreshed/created')
