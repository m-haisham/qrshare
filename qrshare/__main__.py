import click
from qrshare.network import Network


@click.command()
@click.argument('path', required=True)
@click.option('--port', default=4000, type=int, help='waitress server port')
def serve(path, port):
    Network.serve(path, port)


if __name__ == '__main__':
    serve()
