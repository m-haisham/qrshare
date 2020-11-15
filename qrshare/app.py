from pathlib import Path
from typing import List

import waitress
from flask import Flask, render_template, Markup, abort

from .models import Route
from .tools import QrTools


class App:
    def __init__(self, paths: List[Path]):
        self.app = Flask(__name__)
        self.paths = paths
        self.routes = [Route(path) for path in self.paths]
        self.route_map = {route.general_path().lstrip('/'): route for route in self.routes}
        self.accesspoint = '/accesspoint'

    def create_endpoints(self):

        @self.app.route('/')
        def home():
            return render_template(
                'main.html',
                name='root',
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
                    path = sub_route.general_path().lstrip('/')
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