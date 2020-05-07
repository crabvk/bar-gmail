#!/usr/bin/env python

import os
import sys
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

DIR = os.path.dirname(os.path.realpath(__file__))
CREDENTIALS_PATH = os.path.join(DIR, 'credentials.json')

try:
    creds = Credentials.from_authorized_user_file(CREDENTIALS_PATH)
except FileNotFoundError:
    sys.exit('File ' + CREDENTIALS_PATH + ' not found. Run auth.py to obtain credentials.')
gmail = build('gmail', 'v1', credentials=creds)
labels = gmail.users().labels().list(userId='me').execute()
for label in labels['labels']:
    print(label['id'])
