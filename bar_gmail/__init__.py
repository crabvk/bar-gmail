import sys
import argparse
from pathlib import Path
from bar_gmail.gmail import Gmail
from bar_gmail.app import Application, UrgencyLevel
from bar_gmail.printer import WaybarPrinter, PolybarPrinter


def cli():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand')
    subparsers.add_parser('auth', help='Authentication.')
    subparsers.add_parser('labels', help='List mailbox labels.')
    parser.add_argument('-f', '--format', choices=['waybar', 'polybar'], default='waybar',
                        help='Print output in specified format [default: waybar].')
    parser.add_argument('-b', '--badge', default='',
                        help='Badge to display in the bar [default: ].')
    parser.add_argument('-c', '--color',
                        help='Text foreground color (only for Polybar).')
    parser.add_argument('-l', '--label', default='INBOX',
                        help="User's mailbox label for unread messages count [default: INBOX].")
    parser.add_argument('-s', '--sound',
                        help='Notification sound (event sound ID from canberra-gtk-play).')
    parser.add_argument('-u', '--urgency', choices=['low', 'normal', 'critical'],
                        default='normal', help='Notification urgency level [default: normal].')
    parser.add_argument('-t', '--expire-time', type=int,
                        help='The duration, in milliseconds, for the notification to appear on screen.')
    parser.add_argument('-dn', '--no-notify', action='store_true',
                        help='Disable new email notifications.')
    args = parser.parse_args()

    if args.color is not None and args.format != 'polybar':
        parser.error('`--color COLOR` can be used only with `--format polybar`.')

    BASE_DIR = Path(__file__).resolve().parent
    CLIENT_SECRETS_PATH = Path(BASE_DIR, 'client_secrets.json')
    CACHE_DIR = Path(Path.home(), '.cache/bar-gmail')
    CREDENTIALS_PATH = Path(CACHE_DIR, 'credentials.json')
    SESSION_PATH = Path(CACHE_DIR, 'session.json')

    if not CACHE_DIR.is_dir():
        CACHE_DIR.mkdir(exist_ok=True)

    gmail = Gmail(CLIENT_SECRETS_PATH, CREDENTIALS_PATH)

    if args.subcommand == 'auth':
        if gmail.authenticate():
            print('Authenticated successfully.')
        exit()

    if not CREDENTIALS_PATH.is_file():
        print('Credentials not found. Run `bar-gmail auth` for authentication.', file=sys.stderr)
        exit(1)

    if args.subcommand == 'labels':
        for label in gmail.get_labels():
            print(label)
        exit()

    if args.format == 'waybar':
        printer = WaybarPrinter(badge=args.badge)
    elif args.format == 'polybar':
        printer = PolybarPrinter(badge=args.badge, color=args.color)

    app = Application(SESSION_PATH, gmail, printer,
                      badge=args.badge,
                      color=args.color,
                      label=args.label,
                      sound_id=args.sound,
                      urgency_level=UrgencyLevel(args.urgency),
                      expire_time=args.expire_time,
                      is_notify=not args.no_notify)
    app.run()


if __name__ == '__main__':
    cli()
