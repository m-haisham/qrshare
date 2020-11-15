from pathlib import Path
from typing import Tuple, List
from urllib.parse import quote
from uuid import uuid4

from flask import Flask, render_template_string, send_file
from waitress import serve

from .qr import QRCode


class Network:

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