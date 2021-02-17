from io import BytesIO
from pathlib import Path
from typing import List

import waitress
from flask import Flask, send_from_directory, abort, send_file, render_template

from .meta import __version__
from .auth import Authentication
from .models import Route, QRContainer, ZipContent
from .search import Search
from .tools import NetworkTools

class App:
    cache_timeout = 300

    def __init__(self, paths: List[Path], code=None, port=5000):
        self.app = self.init()
        self.auth = Authentication(self.app, code)
        self.search = Search(self, self.auth)

        self.paths = paths
        self.port = port

        self.qr = QRContainer(f'{NetworkTools.local_ip()}:{self.port}')
        self.routes = sorted([Route(path) for path in self.paths], key=lambda r: (r.is_file, r.general_path()))
        self.route_map = {
            route.general_path(False, True).lstrip('/'): route
            for route in self.routes
        }

    def init(self) -> Flask:
        app = Flask(
            __name__,
            instance_relative_config=True,
            template_folder='client/public',
            static_folder='client/public/static'
        )

        app.secret_key = 'entwicklung'  # development key

        # load config for deployment environments
        app.config.from_pyfile('config.py', silent=True)

        app.config['TRAP_HTTP_EXCEPTIONS'] = True
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

        return app

    def create_endpoints(self):

        @self.app.errorhandler(Exception)
        def error_handler(error):
            try:
                return render_template('error.html', code=error.code, name=error.name,  message=error.description),\
                       error.code
            except:
                return render_template('error.html', code=500, message="Something went wrong"), 500

        @self.app.route('/')
        @self.auth.require_auth
        def home():
            return send_from_directory('client/public', 'index.html')

        @self.app.route('/meta')
        def meta():
            return {
                'ip': f'{NetworkTools.local_ip()}:{self.port}',
                'version': __version__,
                'login': bool(self.auth.code),
            }

        @self.app.route('/root')
        @self.auth.require_auth
        def root():
            return {
                'name': '~/',
                'isRoot': True,
                'routes': [r.to_dict() for r in self.routes],
                'parent': None,
                'zip': '/root.zip',
            }

        @self.app.route('/root.zip')
        @self.auth.require_auth
        def zip():
            zipper = ZipContent(self.paths)
            # write the marked files into zip
            zipper.write()
            zipper.reset_hand()

            return send_file(zipper.file, mimetype='application/zip')

        @self.app.route('/svg')
        def svg():
            svg_io = BytesIO()
            self.qr.write(self.qr.string, svg_io)
            svg_io.seek(0)
            return send_file(svg_io, mimetype='image/svg+xml', cache_timeout=self.cache_timeout)

        @self.app.route('/<path:path>')
        def depend(path):
            # TODO create a whitelist
            return send_from_directory('client/public', path)

        @self.app.route('/path/<path:path>')
        @self.auth.require_auth
        def general_access_point(path):
            try:
                route = self.route_map[path]
            except KeyError:
                return abort(404)

            self.map(route)

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

        # create endpoints from other modules
        self.auth.create_endpoints()
        self.search.create_endpoints()

    def map(self, route):
        # check whether sub routes need refreshing
        if route.populate():
            # add newly explored routes to map
            for sub_route in route.sub_routes:
                # make it english; remove the url specific encoding
                path = sub_route.general_path(False, True).lstrip('/')
                self.route_map[path] = sub_route

    def serve(self, debug=False):
        self.create_endpoints()

        if debug:
            self.app.debug = True
            self.app.run(port=self.port, use_reloader=False)
        else:
            waitress.serve(self.app, port=self.port, _quiet=True)
