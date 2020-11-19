# QR share

[![PyPI version](https://badge.fury.io/py/qrshare.svg)](https://badge.fury.io/py/qrshare)

Serve a file on local network and give the url in qrcode form on console

For extra security provide a password `--password [password]`

## Install

```bash
pip install qrshare
```

## Usage

### Send to

Press `Windows` + `r` and enter `shell:sendto`

> C:\Users\(user)\AppData\Roaming\Microsoft\Windows\SendTo

Create shortcut with command `qrshare` in folder

now option qrshare should appear when you right click to a file

### Commandline

```bash
qrshare --help
```

```bash
Usage: __main__.py [OPTIONS] PATHS...

Options:****
  -p, --password TEXT  when provided every device require authentication
  --port INTEGER       waitress server port
  --help               Show this message and exit.
```

### Code Example

```python
from qrshare import App

app = App(paths)
app.serve(True)
```
