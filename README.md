# Polybar Gmail

A [Polybar](https://github.com/jaagr/polybar) module to show unread messages from Gmail.

![preview](https://github.com/vyachkonovalov/polybar-gmail/raw/master/preview.png)

## Dependencies

```sh
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# or use poetry
```

**Font Awesome** - default email icon

**canberra-gtk-play** - new email sound notification

You can change the icon or turn off sound, for more info see [script arguments](#script-arguments)

## Installation

```sh
cd ~/.config/polybar
curl -LO https://github.com/vyachkonovalov/polybar-gmail/archive/master.tar.gz
tar zxf master.tar.gz && rm master.tar.gz
mv polybar-gmail-master gmail
```

and obtain/refresh credentials

```sh
~/.config/polybar/gmail/auth.py -c <rgb-color>
```

You can add multiple credentials using

```sh
~/.config/polybar/gmail/auth.py -addaccount -c <rgb-color>
```

## Auth arguments

`-a` or `--addaccount` - to add a new account. If not set, each credential stored will be checked for expiration and asked for refresh if needed

`-c` or `--color` - set credential email icon color for notification, default: #e06c75

### Module

```ini
[module/gmail]
type = custom/script
exec = python3 ~/.config/polybar/gmail/launch.py --prefix 
interval = 5
click-left = xdg-open https://mail.google.com
```

## Script arguments

`-l` or `--label` - set user's mailbox [label](https://developers.google.com/gmail/api/v1/reference/users/labels/list), default: INBOX

`-p` or `--prefix` - set email icon, default: 

`-ns` or `--nosound` - turn off new email sound

### Example

```sh
./launch.py --label 'CATEGORY_PERSONAL' --prefix '✉' --nosound
```

## Get list of all your mailbox labels

```python
./list_labels.py
```
