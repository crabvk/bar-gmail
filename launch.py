#!/usr/bin/env python

import os
import argparse
import subprocess
from pathlib import Path
from googleapiclient import discovery, errors
from google.oauth2.credentials import Credentials
from httplib2 import ServerNotFoundError

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--label', default='INBOX')
parser.add_argument('-p', '--prefix', default='\uf0e0')
parser.add_argument('-c', '--color', default='#e06c75')
parser.add_argument('-t', '--text-color', default='#ffffff')
parser.add_argument('-ns', '--nosound', action='store_true')
args = parser.parse_args()

DIR = Path(__file__).resolve().parent
PREV_COUNT_DIR = '/dev/shm/mail_count'
CREDENTIALS_PATH = Path(DIR, 'credentials.json')

unread_prefix = '%{F' + args.color + '}' + args.prefix + ' %{F-}'
error_prefix = '%{F' + args.color + '}\uf06a %{F-}'

def print_color(s, c):
    return '%{F' + c + '}' + s + ' %{F-}'

def print_count(count, is_odd=False):
    tilde = '~' if is_odd else ''
    output = ''
    if count > 0:
        output = print_color(args.prefix, args.color) + print_color(tilde + str(count), args.text_color)
    else:
        output = (args.prefix + ' ' + tilde).strip()
    print(output, flush=True)

def update_count(count_was):
    creds = Credentials.from_authorized_user_file(CREDENTIALS_PATH)
    gmail = discovery.build('gmail', 'v1', credentials=creds)
    labels = gmail.users().labels().get(userId='me', id=args.label).execute()
    count = labels['messagesUnread']
    print_count(count)
    if not args.nosound and count_was < count and count > 0:
        subprocess.run(['canberra-gtk-play', '-i', 'message'])
        update_curr_count(count)
    return count

def update_curr_count(count):
    with open(PREV_COUNT_DIR, 'w+') as f:
        try:
            f.write(str(count))
        except:
            return 0


def read_prev_count():
    with open(PREV_COUNT_DIR, 'w+') as f:
        try:
            return int(f.read())
        except:
            return 0

try:
    if Path(CREDENTIALS_PATH).is_file():
        count_was = read_prev_count()
        count_is = update_count(count_was)
    else:
        print(error_prefix + 'credentials not found', flush=True)
except errors.HttpError as error:
    if error.resp.status == 404:
        print(error_prefix + f'"{args.label}" label not found', flush=True)
    else:
        print_count(count_is, True)
except (ServerNotFoundError, OSError):
    print_count(count_is, True)

