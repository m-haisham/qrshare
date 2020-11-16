from pathlib import Path
from typing import List

import waitress
from flask import Flask, render_template, Markup, abort, send_file

from .auth import Authentication
from .models import Route, QRContainer, ZipContent
from .tools import NetworkTools


class App:
    def __init__(self, paths: List[Path], code=None, port=5000):
        self.app = self.init()
        self.auth = Authentication(self.app, code)

        self.paths = paths
        self.port = port

        self.qr = QRContainer(f'{NetworkTools.local_ip()}:{self.port}')
        self.routes = sorted([Route(self.qr, path) for path in self.paths], key=lambda r: (r.is_file, r.general_path()))
        self.route_map = {
            route.general_path(False, True).lstrip('/'): route
            for route in self.routes
        }

    def init(self) -> Flask:
        app = Flask(__name__, instance_relative_config=True)
        app.secret_key = 'entwicklung'  # development key

        # load config for deployment environments
        app.config.from_pyfile('config.py', silent=True)

        return app

    def create_endpoints(self):

        @self.app.route('/')
        @self.auth.require_auth
        def home():
            return render_template(
                'main.html',
                name='~/',
                is_root=True,
                routes=self.routes,
                parent=None,
                zip='/root.zip',
                svg=Markup(self.qr.svg),
                local_link=str(self.qr),
            )

        @self.app.route('/root.zip')
        @self.auth.require_auth
        def zip():
            zipper = ZipContent(self.paths)
            # write the marked files into zip
            zipper.write()
            zipper.reset_hand()

            return send_file(zipper.file, mimetype='application/zip')

        @self.app.route('/path/<path:path>')
        @self.auth.require_auth
        def general_access_point(path):
            try:
                route = self.route_map[path]
            except KeyError:
                return abort(404)

            # check whether sub routes need refreshing
            if route.populate():
                # add newly explored routes to map
                for sub_route in route.sub_routes:
                    # make it english; remove the url specific encoding
                    path = sub_route.general_path(False, True).lstrip('/')
                    self.route_map[path] = sub_route

            return route.get()

        @self.app.route('/zip/<path:path>')
        @self.auth.require_auth
        def zip_access_point(path):
            try:
                route = self.route_map[path.rstrip('.zip')]
            except KeyError:
                return abort(404)

            route.populate()

            return route.zip()

    def serve(self, debug=False):
        self.create_endpoints()

        if debug:
            self.app.debug = True
            self.app.run(port=self.port)
        else:
            waitress.serve(self.app, port=self.port, _quiet=True)
