from pathlib import Path

from qrshare import App

paths = [
    Path(r'C:\Users\User\Documents\Projects\Web\share\index.html'),
    Path(r'C:\Users\User\Documents\Projects'),
]

if __name__ == '__main__':
    app = App(paths, port=8080, code='1234')

    app.serve(True)
