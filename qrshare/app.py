import json
import re
from io import BytesIO
from pathlib import Path
from typing import List

import waitress
from flask import Flask, send_from_directory, abort, send_file, request, Response, render_template

from .auth import Authentication
from .models import Route, QRContainer, ZipContent
from .tools import NetworkTools


class App:
    cache_timeout = 300

    def __init__(self, paths: List[Path], code=None, port=5000):
        self.app = self.init()
        self.auth = Authentication(self.app, code)

        self.paths = paths
        self.port = port

        self.qr = QRContainer(f'{NetworkTools.local_ip()}:{self.port}')
        self.routes = sorted([Route(path) for path in self.paths], key=lambda r: (r.is_file, r.general_path()))
        self.route_map = {
            route.general_path(False, True).lstrip('/'): route
            for route in self.routes
        }

    def init(self) -> Flask:
        app = Flask(__name__, instance_relative_config=True)
        app.secret_key = 'entwicklung'  # development key

        # load config for deployment environments
        app.config.from_pyfile('config.py', silent=True)

        app.config['TRAP_HTTP_EXCEPTIONS']=True
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

        return app

    def create_endpoints(self):

        @self.app.errorhandler(Exception)
        def error_handler(error):
            try:
                return render_template('error.html', code=error.code, message=str(error)), error.code
            except:
                return render_template('client/public/error.html', code=500, message="Something went wrong"), 500

        @self.app.route('/')
        @self.auth.require_auth
        def home():
            return send_from_directory('client/public', 'index.html')

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

        @self.app.route('/search', methods=['GET', 'POST'])
        @self.auth.require_auth
        def search_point():
            # query parameters
            query = request.args.get('query')
            path = request.args.get('path') or '/'
            try:
                limit = int(request.args.get('limit') or 200)
            except ValueError as e:
                return e

            # get routes
            search_routes = []
            if path == '/':
                search_routes.extend(self.routes)
            else:
                try:
                    route = self.route_map[path]
                    search_routes.append(route)
                except KeyError:
                    return abort(403)

            # remove all file routes
            search_routes = [route for route in search_routes if not route.path.is_file()]

            # single char words would makes s... search complicated
            words = [word for word in query.split(' ') if len(word) > 1]

            # regex matcher
            rx = re.compile(
                '|'.join(words),
                re.IGNORECASE
            )

            def generate():
                count = 1
                while True:
                    try:
                        route = search_routes.pop(0)
                    except IndexError:
                        break

                    # get sub routes and queue to be searched
                    self.map(route)

                    if not route.is_file:
                        search_routes.extend(route.sub_routes)

                    # check if current route matches search parameter
                    result = rx.search(route.name)
                    if result:
                        data = route.to_dict()
                        data['matches'] = result.regs
                        data['parent'] = route.parent.to_dict()

                        yield f'data: {json.dumps(data)}\n\n'

                        # limit search space
                        count += 1
                        if count > limit:
                            return

            return Response(generate(), mimetype='text/event-stream')


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
