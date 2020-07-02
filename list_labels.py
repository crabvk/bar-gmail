#!/usr/bin/env python

import sys
import json
from pathlib import Path
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

DIR = Path(__file__).resolve().parent
CREDENTIALS_PATH = Path(DIR, 'credentials.json')

if Path(CREDENTIALS_PATH).is_file():
    with open(CREDENTIALS_PATH, 'r') as f:
        credentials = json.load(f)
    f.close()
    for i in range(0, credentials["count"]):
        print("Loading available tags for account n#" + str(i) + ' \'' + credentials["creds"][i]["tag"] + '\'')
        creds = Credentials.from_authorized_user_info(credentials["creds"][i]["cred"])
        gmail = build('gmail', 'v1', credentials=creds)
        labels = gmail.users().labels().list(userId='me').execute()
        for label in labels['labels']:
            print(label['id'])
else:
    print('File ' + CREDENTIALS_PATH + ' not found. Run auth.py to obtain credentials.')
