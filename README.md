# Bar Gmail

![preview](https://github.com/crabvk/polybar-gmail/raw/master/preview.png)

Get notifications and unread messages count from Gmail (Waybar/Polybar module).

## Dependencies

* Font Awesome: default badge 
* Libnotify: new email notifications, can be disabled with `--no-notify` flag.
* Libcanberra: notification sound (optional).

To display notifications you must have a [notification daemon](https://wiki.archlinux.org/title/Desktop_notifications#Notification_servers) running on your system.

## Installation

Use one of the following methods.

### AUR package on ArchLinux and derivatives

https://aur.archlinux.org/packages/bar-gmail/

### With pip from pypi.org

```sh
pip install --user bar-gmail
~/.local/bin/bar-gmail
```

Depending on your system you may also need to add the `--break-system-packages` flag.

### With pip from git repo

```sh
git clone https://github.com/crabvk/bar-gmail.git
cd bar-gmail
git describe --abbrev=0 --tags # Get latest tag.
git checkoug LATEST_TAG
pip install -e .
~/.local/bin/bar-gmail
```

## Usage

First, you need to authenticate the client:

```sh
bar-gmail auth
```

Then just run `bar-gmail` or `bar-gmail --format polybar` periodically to get unread messages count and new message notifications.
Credentials and session are stored in *~/.cache/bar-gmail*.

## Waybar config example

*~/.config/waybar/config*

```json
"modules-right": {
    "custom/gmail"
}

"custom/gmail": {
    "exec": "bar-gmail",
    "return-type": "json",
    "interval": 10,
    "tooltip": false,
    "on-click": "xdg-open https://mail.google.com/mail/u/0/#inbox"
}
```

*~/.config/waybar/style.css*

```css
#custom-gmail.unread {
    color: white;
}
#custom-gmail.inaccurate {
    color: darkorange;
}
#custom-gmail.error {
    color: darkred;
}
```

## Polybar config example

```ini
modules-right = gmail
...
[module/gmail]
type = custom/script
exec = bar-gmail -f polybar
interval = 10
click-left = xdg-open https://mail.google.com/mail/u/0/#inbox
```

## Script arguments

See `bar-gmail --help` for the full list of available subcommands and command arguments.
Possible values for `-s`, `--sound` can be obtained with:

```shell
ls /usr/share/sounds/freedesktop/stereo/ | cut -d. -f1
```

for example `bar-gmail --sound message-new-instant`.
