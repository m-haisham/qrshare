from pathlib import Path
from urllib.parse import unquote
from typing import List

import waitress
from flask import Flask, render_template, Markup, abort

from .models import Route
from .tools import QrTools


class App:
    def __init__(self, paths: List[Path]):
        self.app = Flask(__name__)
        self.paths = paths
        self.routes = sorted([Route(path) for path in self.paths], key=lambda r: (r.is_file, r.general_path()))
        self.route_map = {
            unquote(route.general_path().lstrip('/')): route
            for route in self.routes
        }

    def create_endpoints(self):

        @self.app.route('/')
        def home():
            return render_template(
                'main.html',
                name='~/',
                is_root=True,
                routes=self.routes,
                parent=None,
                zip='/zip',
                svg=Markup(QrTools.to_svg('asadsadas'))
            )

        @self.app.route('/zip')
        def zip():
            pass

        @self.app.route('/<path:path>')
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
                    path = unquote(sub_route.general_path().lstrip('/'))
                    self.route_map[path] = sub_route

            return route.get()

        @self.app.route('/zip/<path:path>')
        def zip_access_point(path):
            try:
                route = self.route_map[path]
            except KeyError:
                return abort(404)

            route.populate()

            return route.zip()

    def serve(self, debug=False):
        self.create_endpoints()

        if debug:
            self.app.run()
        else:
            waitress.serve(self.app, _quiet=True)