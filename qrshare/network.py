from pathlib import Path
from urllib.parse import quote
from socket import socket, AF_INET, SOCK_DGRAM
from typing import Tuple

from flask import Flask, send_file
from waitress import serve

from .qr import QRCode


class Network:
    LOCALHOST_ADDRESS = "127.0.0.1"

    @staticmethod
    def app(path: str, port: int) -> Tuple[Flask, str]:
        """
        :param path: absolute path to file you want to share
        :param port: port where server runs
        :return: app, url to file
        """
        # ensure path exists and and is a file
        file = Path(path)
        if not file.exists():
            raise FileNotFoundError(f'"{path}" does not exist')
        elif not file.is_file():
            raise FileNotFoundError(f'"{path}" is not a file')

        # get absolute path to file
        file = file.resolve()

        # create route paths
        local_ip = Network.local_ip()

        share_route = f'file/{quote(file.stem)}'
        share_url = f'{local_ip}:{port}/{share_route}'

        # create app and access point
        app = Flask(__name__)

        @app.route(f'/file/{file.stem}')
        def transfer_file():
            return send_file(file)

        return app, share_url

    @staticmethod
    def serve(path: str, port: int = 4000):
        """
        Creates and runs a waitress server where file[path] exposed

        :param path: absolute path to file you want to share
        :param port: port where server runs
        :return:
        """
        app, url = Network.app(path, port)

        print(QRCode(url.encode('utf-8')))
        print("Scan the QR code above.")

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
