# QR share

[![PyPI version](https://badge.fury.io/py/qrshare.svg)](https://badge.fury.io/py/qrshare)

<p float="left" align="middle">
  <img title="login screen" src="https://raw.githubusercontent.com/mHaisham/qrshare/master/.github/images/login.png" width="24%" />
  <img title="home screen" src="https://raw.githubusercontent.com/mHaisham/qrshare/master/.github/images/home.png" width="24%" />
  <img title="search screen" src="https://raw.githubusercontent.com/mHaisham/qrshare/master/.github/images/search.png" width="24%" />
  <img title="qrcode screen" src="https://raw.githubusercontent.com/mHaisham/qrshare/master/.github/images/qr.png" width="24%" />
</p>

Serve a file on local network and give the url in qrcode form on console

For extra security provide a password `--password [password]`

## Install

```bash
pip install qrshare
```

## Usage

### Send to

> Windows only

Creating a shortcut in `shell:sendto` provides for easier use of convenience

#### commandline

```bash
qrshare config --sendto
```

#### manually

Press `Windows` + `r` and enter `shell:sendto`

> %USERPROFILE%\AppData\Roaming\Microsoft\Windows\SendTo

Create shortcut with command `qrshare serve` in folder

now option qrshare should appear when you right click to a file

### Commandline

> `qrshare --help`

```bash
Usage: __main__.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  config  change user configurations
  serve   serve given list paths as per given options
```

> `qrshare serve --help`

```bash
Options:
  -p, --password TEXT  when provided every device require authentication
  --port INTEGER       waitress server port
  --help               Show this message and exit.
```

- `password` is given preference over global password

> `qrshare config --help`

```bash
Options:
  -p, --password TEXT  set a global password
  --remove-password    remove currently set global password
  --sendto             reset windows 'Send To' shortcut
  --open               open config directory
  --help               Show this message and exit.
```

- `global password` can be removed by setting it an empty string ("")


### Code Example

```python
from qrshare import App

app = App(paths)
app.serve(True)
```
