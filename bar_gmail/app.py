import os
import json
import time
from enum import Enum
from pathlib import Path
from subprocess import Popen
from gi.repository import GLib
from dasbus.connection import SessionMessageBus
from dasbus.error import DBusError
from google.auth.exceptions import TransportError
from googleapiclient.errors import HttpError
from bar_gmail.gmail import Gmail
from bar_gmail.printer import WaybarPrinter, PolybarPrinter

APP_NAME = 'Bar Gmail'
NOTIFICATION_CATEGORY = 'email.arrived'
BASE_DIR = Path(__file__).resolve().parent
GMAIL_ICON_PATH = Path(BASE_DIR, 'gmail_icon.svg')


class UrgencyLevel(Enum):
    LOW = 0
    NORMAL = 1
    CRITICAL = 2


class Application:
    def __init__(self, session_path: Path, gmail: Gmail, printer: WaybarPrinter | PolybarPrinter,
                 label: str, sound_id: str, urgency_level: UrgencyLevel, expire_timeout: int,
                 is_notify: bool):
        self.session_path = session_path
        self.gmail = gmail
        self.printer = printer
        self.label = label
        self.sound_id = sound_id
        self.urgency_level = urgency_level
        self.expire_timeout = expire_timeout
        self.is_notify = is_notify

    @staticmethod
    def _is_innacurate(since: float) -> bool:
        # Data older than 5 minutes is considered innacurate.
        return time.time() - since > 300

    def _play_sound(self):
        try:
            Popen(['canberra-gtk-play', '-i', self.sound_id], stderr=open(os.devnull, 'wb'))
        except FileNotFoundError:
            pass

    def _send_notifications(self, messages):
        try:
            bus = SessionMessageBus()
            proxy = bus.get_proxy(
                'org.freedesktop.Notifications',
                '/org/freedesktop/Notifications'
            )

            app_icon = str(GMAIL_ICON_PATH)
            replaces_id = 0
            actions = []

            # https://lazka.github.io/pgi-docs/GLib-2.0/classes/VariantType.html#GLib.VariantType
            hints = {
                'category': GLib.Variant('s', NOTIFICATION_CATEGORY),
                'urgency': GLib.Variant('y', self.urgency_level.value),
            }

            for message in messages:
                summary = message['from']
                body = message['subject']

                # https://specifications.freedesktop.org/notification-spec/notification-spec-latest.html
                proxy.Notify(APP_NAME, replaces_id, app_icon, summary,
                             body, actions, hints, self.expire_timeout)
        except DBusError:
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
            if unread != session['unread'] or inaccurate is True:
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
                if any(history['messages']):
                    if self.sound_id:
                        self._play_sound()
                    if self.is_notify:
                        self._send_notifications(history['messages'])
                session['history_id'] = history['history_id']
                with open(self.session_path, 'w') as f:
                    json.dump(session, f)
        except HttpError as error:
            if error.resp.status == 404:
                self.printer.error(f'Label not found: {self.label}')
        except TransportError:
            pass
