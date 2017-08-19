# Polybar Gmail

A [Polybar](https://github.com/jaagr/polybar) module to show unread messages from Gmail.

![screenshot](https://github.com/vyachkonovalov/polybar-gmail/raw/master/preview.png)

## Dependencies

```sh
sudo pip install --upgrade google-api-python-client
```

**Font Awesome** - for email badge

**canberra-gtk-play** - for new email sound

You can change the badge or turn off sound, for more info see [script arguments](#script-arguments)

## Script arguments

`-p` or `--prefix` - to change email badge

`-c` or `--color` - to change new email badge color

`-ns` or `--nosound` - turn off new email sound

### Example

```sh
launch.py --prefix '📧' --color '#be5046' --nosound
```
