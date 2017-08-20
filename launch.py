#!/usr/bin/env python

import os
import pathlib
import subprocess
import time
import argparse
from apiclient import discovery, errors
from oauth2client import client, file
from httplib2 import ServerNotFoundError

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--prefix', default='\uf0e0')
parser.add_argument('-c', '--color', default='#e06c75')
parser.add_argument('-ns', '--nosound', action='store_true')
args = parser.parse_args()

DIR = os.path.dirname(os.path.realpath(__file__))
CREDENTIALS_PATH = os.path.join(DIR, 'credentials.json')

unread_prefix = '%{F' + args.color + '}' + args.prefix + ' %{F-}'
error_prefix = '%{F' + args.color + '}\uf06a %{F-}'
count_was = 0

def update_count(count_was):
    gmail = discovery.build('gmail', 'v1', credentials=file.Storage(CREDENTIALS_PATH).get())
    list = gmail.users().messages().list(userId='me', q='in:inbox is:unread').execute()
    count = list['resultSizeEstimate']
    if count > 0:
        print(unread_prefix + str(count), flush=True)
    else:
        print(args.prefix, flush=True)
    if not args.nosound and count_was < count and count > 0:
        subprocess.run(['canberra-gtk-play', '-i', 'message'])
    return count

while True:
    try:
        if pathlib.Path(CREDENTIALS_PATH).is_file():
            count_was = update_count(count_was)
            time.sleep(10)
        else:
            print(error_prefix + 'credentials not found', flush=True)
            time.sleep(2)
    except (errors.HttpError, ServerNotFoundError) as error:
        print(error_prefix + str(error), flush=True)
        time.sleep(5)
    except client.AccessTokenRefreshError:
        print(error_prefix + 'revoked/expired credentials', flush=True)
        time.sleep(5)
