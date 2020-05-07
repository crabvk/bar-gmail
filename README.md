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
~/.config/polybar/gmail/auth.py
```

### Module

```ini
[module/gmail]
type = custom/script
exec = ~/.config/polybar/gmail/launch.py
tail = true
click-left = xdg-open https://mail.google.com
```

## Script arguments

`-l` or `--label` - set user's mailbox [label](https://developers.google.com/gmail/api/v1/reference/users/labels/list), default: INBOX

`-p` or `--prefix` - set email icon, default: 

`-c` or `--color` - set new email icon color, default: #e06c75

`-ns` or `--nosound` - turn off new email sound

### Example

```sh
./launch.py --label 'CATEGORY_PERSONAL' --prefix '✉' --color '#be5046' --nosound
```

## Get list of all your mailbox labels

```python
./list_labels.py
```
