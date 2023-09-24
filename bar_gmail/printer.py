import json


class Printer:
    def _print(self, text):
        try:
            print(text, flush=True)
        except BrokenPipeError:
            pass


class WaybarPrinter(Printer):
    def __init__(self, badge: str):
        self.badge = badge

    def print(self, count, inaccurate=False):
        classes = set()
        text = ''
        if inaccurate:
            classes.add('inaccurate')
        if count > 0:
            classes.add('unread')
            text = str(count)
        text = f'{self.badge} {text}'.strip()
        text = json.dumps({'text': f'{text}', 'class': list(classes)})
        self._print(text)

    def error(self, message):
        text = json.dumps({'text': message, 'class': 'error'})
        self._print(text)


class PolybarPrinter(Printer):
    def __init__(self, badge: str, color: str = None):
        self.badge = badge
        self.color = color

    def print(self, count, inaccurate=False):
        text = str(count) if count > 0 else ''
        if inaccurate:
            text = f'~{text}'
        text = f'{self.badge} {text}'.strip()
        if count > 0 and self.color:
            text = f'%{{F{self.color}}}{text}%{{F-}}'
        self._print(text)

    def error(self, message):
        text = f' {message}'
        if self.color:
            text = f'%{{F{self.color}}}{text}%{{F-}}'
        self._print(text)
