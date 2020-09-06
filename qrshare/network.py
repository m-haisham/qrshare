from uuid import uuid4

from pathlib import Path
from urllib.parse import quote
from socket import socket, AF_INET, SOCK_DGRAM
from typing import Tuple, List

from flask import Flask, render_template_string, send_file
from waitress import serve

from .qr import QRCode
from .template import shared_template


class Network:
    LOCALHOST_ADDRESS = "127.0.0.1"

    @staticmethod
    def app(paths: str, port: int) -> Tuple[Flask, str]:
        """
        :param path: absolute path to file you want to share
        :param port: port where server runs
        :return: app, url to file
        """
        local_ip = Network.local_ip()

        shared = f'shared/{uuid4().fields[-1]}'

        # create file routes
        files = {}
        for path in paths:
            # ensure path exists and and is a file
            file = Path(path)
            if not file.exists():
                raise FileNotFoundError(f'"{path}" does not exist')
            elif not file.is_file():
                raise FileNotFoundError(f'"{path}" is not a file')

            # get absolute path to file
            file = file.resolve()

            # add route
            share_route = f'{shared}/{quote(file.name)}'
            files[file.name] = ({'file': file, 'route': share_route})

        # create app
        app = Flask(__name__)

        @app.route(f'/{shared}')
        def share_home():
            return render_template_string(shared_template, links=files.values())

        @app.route(f'/{shared}/<filename>')
        def share_file(filename):
            return send_file(files[filename]['file'])

        if len(files) == 1:
            # direct link download file
            share_url = f'{local_ip}:{port}/{list(files.values())[0]["route"]}'
        else:
            # go to file list
            share_url = f'{local_ip}:{port}/{shared}'

        return app, share_url

    @staticmethod
    def serve(paths: List[str], port: int = 4000):
        """
        Creates and runs a waitress server where file[path] exposed

        :param path: absolute path to file you want to share
        :param port: port where server runs
        :return:
        """
        app, url = Network.app(paths, port)

        print(QRCode(url.encode('utf-8')))
        print("Scan the QR code above.")
        print(f"local: http://{url}", end='\n\n')

        serve(app, port=port)

    @staticmethod
    def local_ip() -> str:
        local_socket = socket(AF_INET, SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            local_socket.connect(('10.255.255.255', 1))
            ip_address = local_socket.getsockname()[0]
        except:  # noqa: E722
            ip_address = Network.LOCALHOST_ADDRESS
        finally:
            local_socket.close()

        if ip_address == Network.LOCALHOST_ADDRESS:
            raise ConnectionError(
                "Could find valid IP address for a local network. "
                "Verify that you are connected to a router.")

        return ip_address
