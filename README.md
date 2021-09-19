# qrshare

![PyPI](https://img.shields.io/pypi/v/qrshare)
![Python Version](https://img.shields.io/badge/Python-v3.6-blue)
![Repo Size](https://img.shields.io/github/repo-size/mHaisham/qrshare)
[![Contributors](https://img.shields.io/github/contributors/mHaisham/qrshare)](https://github.com/mHaisham/qrshare/graphs/contributors)
![Last Commit](https://img.shields.io/github/last-commit/mHaisham/qrshare/master)
![Issues](https://img.shields.io/github/issues/mHaisham/qrshare)
![Pull Requests](https://img.shields.io/github/issues-pr/mHaisham/qrshare)
[![License](https://img.shields.io/github/license/mHaisham/qrshare)](LICENSE)

Serve files or folders on local network with ease.

<p float="left" align="middle">
  <img title="login screen" src="https://raw.githubusercontent.com/mHaisham/qrshare/master/.github/images/login.png" width="24%" />
  <img title="home screen" src="https://raw.githubusercontent.com/mHaisham/qrshare/master/.github/images/home.png" width="24%" />
  <img title="search screen" src="https://raw.githubusercontent.com/mHaisham/qrshare/master/.github/images/search.png" width="24%" />
  <img title="qrcode screen" src="https://raw.githubusercontent.com/mHaisham/qrshare/master/.github/images/qr.png" width="24%" />
</p>

For extra security provide a password `--password [password]`

## Install

```bash
pip install qrshare
```

### Termux

1. Install [Termux] from [F-Droid].

2. Update packages: `apt update && apt upgrade`

3. Setup storage: `termux-setup-storage`

4. Install Python: `pkg install python`

5. Install qrshare: `pip install qrshare`

6. Use as described below in [Terminal].

[Termux]: https://termux.com/
[F-Droid]: https://f-droid.org/en/packages/com.termux/
[Terminal]: https://github.com/mHaisham/qrshare#terminal

## Usage

### Terminal

Serve a specific directory or file

```bash
qrshare serve path/to/share
```

Serve the current directory

```bash
qrshare serve .
```

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

now option qrshare should appear when you right click to a file or folder

### Commandline

#### `qrshare --help`

```bash
Usage: __main__.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  config  change user configurations
  serve   serve given list paths as per given options
```

#### `qrshare serve --help`

```bash
Usage: __main__.py serve [OPTIONS] PATHS...

  serve given list paths as per given options

Options:
  -p, --password TEXT  when provided every device require authentication
  --port INTEGER       waitress server port
  --help               Show this message and exit.
```

- `password` is given preference over global password

#### `qrshare config --help`

```bash
Usage: __main__.py config [OPTIONS]

  change user configurations

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

app = App(paths, debug=True)
app.serve()
```
