from pathlib import Path
from socket import socket, AF_INET, SOCK_DGRAM
from typing import Tuple, List
from urllib.parse import quote
from uuid import uuid4

from flask import Flask, render_template_string, send_file
from waitress import serve

from .qr import QRCode
from .template import shared_template


class Network:
    LOCALHOST_ADDRESS = "127.0.0.1"

    @staticmethod
    def app(paths: List[str], port: int) -> Tuple[Flask, str, str]:
        """
        :param paths: absolute path to file you want to share (one or more)
        :param port: port where server runs
        :return: app, url to file
        """
        local_ip = Network.local_ip()

        ukey = str(uuid4().fields[-1])

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
            share_route = f'{ukey}/{quote(file.name)}'
            files[file.name] = ({'file': file, 'route': share_route})

        # create app
        app = Flask(__name__)

        @app.route(f'/{ukey}')
        def share_home():
            return render_template_string(shared_template, links=files.values())

        @app.route(f'/{ukey}/<filename>')
        def share_file(filename):
            return send_file(files[filename]['file'])

        link = f'{local_ip}:{port}/{ukey}'
        if len(files) == 1:
            # direct link download file
            share_url = f'{local_ip}:{port}/{list(files.values())[0]["route"]}'
        else:
            # go to file list
            share_url = link

        return app, share_url, link

    @staticmethod
    def serve(paths: List[str], port: int = 4000):
        """
        Creates and runs a waitress server where file[path] exposed

        :param paths: absolute path to file you want to share (one or more)
        :param port: port where server runs
        :return:
        """
        app, url, link = Network.app(paths, port)

        print(QRCode(url.encode('utf-8')))
        print("Scan the QR code above.")
        print()
        print(f"Sharing on http://{link}")

        serve(app, port=port, _quiet=True)

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
