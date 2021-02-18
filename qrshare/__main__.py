from pathlib import Path

import click

from qrshare import App, create_shortcut
from qrshare.config import UserConfig

@click.group()
def cli():
    pass


@cli.command()
@click.argument('paths', nargs=-1, required=True)
@click.option('-p', '--password', type=str, help='when provided every device require authentication')
@click.option('--port', default=4000, type=int, help='waitress server port')
def serve(paths, password, port):
    """
    serve given list paths as per given options
    """
    try:
        app = App([Path(path).resolve() for path in paths], password, port)

        qr = app.qr
        print(qr.to_ascii(qr.string))
        print(f'Sharing on http://{qr}')

        app.serve()

    except (FileNotFoundError, ValueError) as e:
        print(e)
        input('Press enter to exit')


@cli.command()
@click.option('-p', '--password', type=str, help='set a global password')
@click.option('--sendto', is_flag=True, help='reset windows \'Send To\' shortcut')
@click.option('--open', 'open_config', is_flag=True, help='open config directory')
def config(password, sendto, open_config):
    """
    change user configurations
    """
    user = UserConfig()

    if sendto:
        # windows send to path
        path = Path.home() / Path(r'AppData\Roaming\Microsoft\Windows\SendTo')

        print(f'Creating shortcut with command \'qrshare\' in {path}...', end=' ')

        try:
            create_shortcut(path, 'qrshare', 'serve')
        except Exception as e:
            print(e)
        else:
            print('done')

    if password:
        user.config.put('password', password)
        print(f'New global password set: {password}')
    elif password == "":
        user.config.put('password', None)
        print('Removed global password')

    if open_config:
        import os
        os.startfile(user.path)


if __name__ == '__main__':
    cli()
