from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient import discovery
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

SCOPE = 'https://www.googleapis.com/auth/gmail.metadata'


class Gmail():
    def __init__(self, client_secrets_path: Path, credentials_path: Path):
        self.client_secrets_path = client_secrets_path
        self.credentials_path = credentials_path
        self._credentials = None
        self._gmail = None

    @property
    def credentials(self):
        if self._credentials is None:
            self._credentials = Credentials.from_authorized_user_file(self.credentials_path)
        return self._credentials

    @property
    def gmail(self):
        if self._gmail is None:
            self._gmail = discovery.build('gmail', 'v1', credentials=self.credentials)
        return self._gmail

    @staticmethod
    def _filter_headers(headers: list) -> dict:
        result = {}
        for header in headers:
            if header['name'] == 'From' or header['name'] == 'Subject':
                result[header['name']] = header['value']
        return result

    def authenticate(self) -> bool:
        flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets_path, scopes=SCOPE)
        creds = flow.run_local_server(open_browser=False)
        with open(self.credentials_path, 'w') as creds_file:
            creds_file.write(creds.to_json())
            return True

    def get_labels(self) -> list[str]:
        gmail = discovery.build('gmail', 'v1', credentials=self.credentials)
        labels = gmail.users().labels().list(userId='me').execute()
        return list(map(lambda label: label['id'], labels['labels']))

    def get_latest_history_id(self) -> int | None:
        messages = self.gmail.users().messages().list(userId='me', maxResults=1).execute()
        if any(messages['messages']):
            message_id = messages['messages'][0]['id']
            message = self.gmail.users().messages().get(userId='me', id=message_id, format='metadata').execute()
            return message['historyId']

    def get_history_since(self, history_id: str) -> dict:
        messages = []
        history = self.gmail.users().history().list(userId='me', startHistoryId=history_id,
                                                    historyTypes=['messageAdded']).execute()
        for record in history.get('history', []):
            for message in record.get('messagesAdded', []):
                if 'UNREAD' not in message['message']['labelIds']:
                    continue
                message_id = message['message']['id']
                try:
                    response = self.gmail.users().messages().get(userId='me', id=message_id, format='metadata').execute()
                    headers = self._filter_headers(response['payload']['headers'])
                    messages.append(headers)
                except HttpError as error:
                    # Requested message was not found.
                    if error.resp.status == 404:
                        pass
        return {
            'messages': messages,
            'history_id': history['historyId']
        }

    def get_unread_messages_count(self, label: str = 'INBOX'):
        labels = self.gmail.users().labels().get(userId='me', id=label).execute()
        return labels['messagesUnread']

    # TODO: Save refreshed credentials.
    def refresh_credentials(self) -> bool:
        if self.credentials.expired:
            self.credentials.refresh(Request())
            return True
        return False
