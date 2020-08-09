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
        local_ip = Network.local_ip()

        file = Path(path)
        share_route = f'file/{quote(file.stem)}'
        share_url = f'{local_ip}:{port}/{share_route}'

        app = Flask(__name__)

        @app.route(f'/file/{file.stem}')
        def transfer_file():
            return send_file(file)

        return app, share_url

    @staticmethod
    def serve(path: str, port: int = 4000):
        app, url = Network.app(path, port)

        print(QRCode(url))
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
