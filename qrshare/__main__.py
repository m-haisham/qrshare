import click

from qrshare.network import Network


@click.command()
@click.argument('paths', nargs=-1, required=True)
@click.option('--port', default=4000, type=int, help='waitress server port')
def serve(paths, port):
    try:
        Network.serve(paths, port)
    except (FileNotFoundError, ValueError) as e:
        print(e)
        input('Press enter to exit')


if __name__ == '__main__':
    serve()
