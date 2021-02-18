from io import BytesIO
from pathlib import Path
from typing import List, Optional

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
                return render_template('error.jinja2', code=error.code, name=error.name,  message=error.description),\
                       error.code
            except:
                return render_template('error.jinja2', code=500, message="Something went wrong"), 500

        @self.app.route('/', defaults={'id': 0})
        @self.app.route('/results', defaults={'id': 2})
        @self.app.route('/qrcode', defaults={'id': 4})
        @self.app.route('/more', defaults={'id': 5})
        @self.auth.require_auth
        def home(id):
            return render_template('index.jinja2', id=id)

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
                'href': '/',
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
            return send_from_directory('client/public', path)

        @self.app.route('/path/<path:path>')
        @self.auth.require_auth
        def general_access_point(path):
            try:
                route = self.route_map[path]
            except KeyError:
                route = self.detect(path)

            if route is None:
                return abort(404)

            self.map(route)

            return route.get()

        @self.app.route('/zip/<path:path>')
        @self.auth.require_auth
        def zip_access_point(path):
            path = path.rstrip('.zip')

            try:
                route = self.route_map[path]
            except KeyError:
                route = self.detect(path)

            if route is None:
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

    def detect(self, path) -> Optional[Route]:
        for r in self.routes:
            if r.path.is_file():
                continue

            # check if the requested path is a subdirectory of existing root directories
            if not path.startswith(r.general_path(False, True).strip('/')):
                continue

            requested_path = r.path.parent / path
            if requested_path.exists():

                # make sure root route has been mapped
                self.map(r)

                # the loop below methodically populates all the sub routes leading to requested route
                segments = path.split('/')
                for i in range(2, len(segments)):
                    try:
                        sub_route = self.route_map['/'.join(segments[:i])]
                        self.map(sub_route)
                    except IndexError:
                        break

                return self.route_map[path]

    def serve(self, debug=False):
        self.create_endpoints()

        if debug:
            self.app.debug = True
            self.app.run(port=self.port, use_reloader=False)
        else:
            waitress.serve(self.app, port=self.port, _quiet=True)
