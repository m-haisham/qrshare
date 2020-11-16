from pathlib import Path

import click

from qrshare import App


@click.command()
@click.argument('paths', nargs=-1, required=True)
@click.option('-p', '--password', type=str, help='when provided every device require authentication')
@click.option('--port', default=4000, type=int, help='waitress server port')
def serve(paths, password, port):
    try:
        app = App([Path(path).resolve() for path in paths], password, port)

        qr = app.qr
        print(qr.to_ascii(qr.string))
        print(f'Sharing on http://{qr}')

        app.serve()

    except (FileNotFoundError, ValueError) as e:
        print(e)
        input('Press enter to exit')


if __name__ == '__main__':
    serve()
