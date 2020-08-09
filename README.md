# QR share

Serve a file on local network and give the url in qrcode form on console

## Install

```bash
git clone "https://github.com/mHaisham/qrshare.git"

cd qrshare

python setup.py install
```

## Usage

### Commandline

```bash
Usage: __main__.py [OPTIONS] PATH

Options:
  --port INTEGER  waitress server port
  --help          Show this message and exit.
```

### Example

```python
from qrshare import Network

Network.serve(ABS_PATH_TO_FILE, port=[OPTIONAL]PORT)
```

