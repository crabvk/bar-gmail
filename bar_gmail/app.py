import os
import json
import time
from enum import Enum
from pathlib import Path
from subprocess import Popen
from bar_gmail.gmail import Gmail
from bar_gmail.printer import WaybarPrinter, PolybarPrinter
from google.auth.exceptions import TransportError
from googleapiclient.errors import HttpError

BASE_DIR = Path(__file__).resolve().parent
GMAIL_ICON_PATH = Path(BASE_DIR, 'gmail_icon.svg')


class UrgencyLevel(Enum):
    LOW = 'low'
    NORMAL = 'normal'
    CRITICAL = 'critical'


class Application:
    def __init__(self, session_path: Path, gmail: Gmail, printer: WaybarPrinter | PolybarPrinter,
                 badge: str, color: str | None, label: str, sound_id: str,
                 urgency_level: UrgencyLevel, expire_time: int, is_notify: bool):
        self.session_path = session_path
        self.gmail = gmail
        self.printer = printer
        self.badge = badge
        self.label = label
        self.sound_id = sound_id
        self.urgency_level = urgency_level
        self.expire_time = expire_time
        self.is_notify = is_notify
        self.color = color
        args = []
        # Set application name.
        args.extend(('-a', 'Bar Gmail'))
        # Set category.
        args.extend(('-c', 'email.arrived'))
        # Set icon.
        args.extend(('-i', GMAIL_ICON_PATH))
        # Set urgency level.
        args.extend(('-u', self.urgency_level.value))
        # Set notification expiration time.
        if self.expire_time is not None:
            args.extend(('-t', self.expire_time))
        self.notification_args = args

    @staticmethod
    def _is_innacurate(since: float) -> bool:
        # Data older than 5 minutes is considered innacurate.
        return time.time() - since > 300

    def _play_sound(self):
        try:
            Popen(['canberra-gtk-play', '-i', self.sound_id], stderr=open(os.devnull, 'wb'))
        except FileNotFoundError:
            pass

    def _send_notification(self, message):
        try:
            Popen(['notify-send', *self.notification_args, message['From'], message['Subject']],
                  stderr=open(os.devnull, 'wb'))
        except FileNotFoundError:
            pass

    def run(self):
        session = {'history_id': None, 'unread': None}
        inaccurate = False
        if self.session_path.is_file():
            with open(self.session_path, 'r') as f:
                session = json.loads(f.read())
                inaccurate = self._is_innacurate(session['time'])
                self.printer.print(session['unread'], inaccurate=inaccurate)

        try:
            unread = self.gmail.get_unread_messages_count(self.label)
            if unread != session['unread'] or inaccurate == True:
                self.printer.print(unread)
            history_id = session['history_id'] or self.gmail.get_latest_history_id()
            session = {
                'history_id': history_id,
                'unread': unread,
                'time': time.time()
            }
            with open(self.session_path, 'w') as f:
                json.dump(session, f)

            if session['history_id']:
                history = self.gmail.get_history_since(session['history_id'])
                if any(history['messages']) and self.sound_id:
                    self._play_sound()
                for message in history['messages']:
                    self._send_notification(message)
                session['history_id'] = history['history_id']
                with open(self.session_path, 'w') as f:
                    json.dump(session, f)
        except HttpError as error:
            if error.resp.status == 404:
                self.printer.error(f'Label not found: {self.label}')
        except TransportError:
            pass
