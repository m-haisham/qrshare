import json
from typing import List, Callable, Union, Optional

from flask import request, Response, abort
from regex import regex

from .auth import Authentication
from .models import Route


class Search:
    def __init__(self, app, auth: Authentication):
        self.app = app
        self.auth = auth
        
        self.create_endpoints()
        
    def create_endpoints(self):

        @self.app.app.route('/search')
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
            search_routes = self.filter_routes(path)

            # single char words would makes s... search complicated
            words = [word for word in query.split(' ') if len(word) > 1]

            # regex matcher
            rx = regex.compile(
                '|'.join(words),
                regex.IGNORECASE
            )

            def predicate(route: Route):
                result = [match for match in rx.finditer(route.name)]
                if result:
                    data: dict = route.to_dict()
                    data['matches'] = [match.regs[0] for match in result]
                    data['parent'] = route.parent.to_dict()
                    data['zip'] = route.zip_path()

                    return data

            return Response(self.generate(search_routes, predicate, limit), mimetype='text/event-stream')

    def filter_routes(self, path: str) -> List[Route]:
        search_routes = []
        if path == '/':
            search_routes.extend(self.app.routes)
        else:
            try:
                search_routes.append(self.app.route_map[path])
            except KeyError:
                return abort(403)

        # remove all file routes
        return [route for route in search_routes if not route.path.is_file()]

    def generate(self, routes: List[Route], predicate=Callable[[Route], Optional[dict]], limit=200):
        count = 1
        while True:
            try:
                route = routes.pop(0)
            except IndexError:
                break

            # get sub routes and queue to be searched
            self.app.map(route)

            if not route.is_file:
                routes.extend(route.sub_routes)

            # check if current route matches search parameter
            data = predicate(route)
            if type(data) == dict:
                yield f'data: {json.dumps(data)}\n\n'

                # limit search space
                count += 1
                if count > limit:
                    return
