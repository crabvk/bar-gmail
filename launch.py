#!/usr/bin/env python3

import os
import argparse
import subprocess
import json
from pathlib import Path
from googleapiclient import discovery, errors
from google.oauth2.credentials import Credentials
from httplib2 import ServerNotFoundError

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--label', default='INBOX')
parser.add_argument('-p', '--prefix', default='\uf0e0')
parser.add_argument('-ns', '--nosound', action='store_true')
args = parser.parse_args()

DIR = Path(__file__).resolve().parent
PREV_COUNT_DIR = '/tmp/mail_count'
CREDENTIALS_PATH = Path(DIR, 'credentials.json')

error_prefix = '%{F' + "#ff0000" + '}\uf06a %{F-}'

prev_read = []

def print_count(count, color, is_odd=False):
    tilde = '~' if is_odd else ''
    output = ''
    if count > 0:
        output = '%{F' + color + '}' + args.prefix + ' %{F-}'
    else:
        #output = (args.prefix + ' ' + tilde).strip()
        output = ''
    return output

def update_count(count_was, creds, color):
    cred = Credentials.from_authorized_user_info(creds)
    gmail = discovery.build('gmail', 'v1', credentials=cred)
    labels = gmail.users().labels().get(userId='me', id=args.label).execute()
    count = labels['messagesUnread']
    aux = print_count(count, color)
    if count_was != count:
        if not args.nosound and count > count_was:
            subprocess.run(['canberra-gtk-play', '-i', 'message'])
    return count, aux

def update_curr_count(counts):
    data = ",".join([str(i) for i in counts])
    with open(PREV_COUNT_DIR, 'w+') as f:
        try:
            f.write(data)
            f.close()
        except:
            f.close()

try:
    n_accounts = 0
    printable = ''
    #Reading credentials
    if Path(CREDENTIALS_PATH).is_file():
        with open(CREDENTIALS_PATH, 'r') as f:
            credentials = json.load(f)
        f.close()
        n_accounts = credentials["count"]
    else:
        print(error_prefix + 'credentials not found', flush=True)
    #Reading previous count
    if Path(PREV_COUNT_DIR).is_file():
        with open(PREV_COUNT_DIR, 'r+') as t:
            prev_read = [int(x) for x in t.read().split(",")]
        t.close()
        # This would be the case of adding a new account when a temp file was already set for less accounts
        if len(prev_read) < n_accounts:
            for i in range(0, n_accounts- len(prev_read)):
                prev_read.append(0)
    else:
        prev_read = [0] * n_accounts
    for i in range(0, n_accounts):
        credential = credentials["creds"][i]
        prev_read[i], aux = update_count(prev_read[i], credential["cred"] ,credential["color"])
        printable += aux + ' '
    print(printable)
    update_curr_count(prev_read)
except errors.HttpError as error:
    if error.resp.status == 404:
        print(error_prefix + f'"{args.label}" label not found', flush=True)
    else:
        print('There was an Http Error')
except (ServerNotFoundError, OSError):
    print('Server not found')
