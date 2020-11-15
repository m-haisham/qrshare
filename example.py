from pathlib import Path

from qrshare import App

paths = [
    Path(r'C:\Users\User\Documents\Projects\Web\share\index.html'),
    Path(r'C:\Users\User\Documents'),
    Path(r'C:\Users\User'),
]

if __name__ == '__main__':
    app = App(paths)
    app.serve(True)

