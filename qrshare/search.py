import json
from typing import List, Callable, Union, Optional, Iterable

from flask import request, Response, abort
from regex import regex
import re

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
            exts = request.args.get('exts')
            types = request.args.get('types')
            path = request.args.get('path') or '/'
            try:
                limit = int(request.args.get('limit') or 200)
            except ValueError as e:
                return e

            # get routes
            search_routes = self.filter_routes(path)

            predicate = self.create_predicate(query, exts, types)

            return Response(self.generator(search_routes, predicate, limit), mimetype='text/event-stream')

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

    def create_predicate(self, query: str = None, exts: Union[str, Iterable[str]] = None, types: Union[str, Iterable[str]] = None) \
            -> Callable[[Route], dict]:

        if not any((bool(query), bool(exts), bool(types))):
            raise ValueError('Require at least one argument (query, exts, types)')

        rx_query = None
        if query is not None:
            # single char words would makes s... search complicated
            words = {word for word in query.split(' ') if len(word) > 1}

            rx_query = regex.compile(
                '|'.join(words),
                regex.IGNORECASE
            )

        rx_exts = None
        if exts is not None:
            if type(exts) == str:
                exts = (exts, )

            # default is type iterable, any other type should be converted to iterable before this point
            # ensure extension has a dot at the start
            exts = {'.' + ext.lstrip('.') for ext in exts}

            rx_exts = regex.compile(
                '|'.join(exts)
            )

        # sanitizing received types
        # :throws: value error if unexpected type removed
        if types is not None:
            if type(types) == str:
                types = (types, )

            # default is type iterable, any other type should be converted to iterable before this point
            for t in types:
                if t not in Route.types:
                    raise ValueError(f'Unexpected value received: {t}; expecting {Route.types}')

            # removes any duplicate values
            types = set(types)

        def predicate(route: Route):

            # filter by path type
            # if no dir types are specified, its assumed all types are welcome
            if types is not None and self._is_route_of_type(route, types):
                return

            matches = []
            relevance = 0

            # relevance increases if there was a type check
            if types != Route.types:
                relevance += 1

            # filter by query
            if rx_query is not None:
                matches += [match.regs[0] for match in rx_query.finditer(route.name)]

            # filter by extension
            if rx_exts is not None and route.is_file():
                # getting the full suffix of the route
                full_suffix = ''.join(route.path.suffixes)
                matches += [match.regs[0] for match in rx_exts.finditer(full_suffix)]

            if matches:
                # number of matches is directly proportional to result relevance
                relevance += len(matches)

                data: dict = route.to_dict()
                data['matches'] = matches
                data['relevance'] = relevance
                data['parent'] = route.parent.to_dict()
                data['zip'] = route.zip_path()

                return data

        return predicate

    def generator(self, routes: List[Route], predicate=Callable[[Route], Optional[dict]], limit=200):
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

    def _is_route_of_type(self, route: Route, types: List[str]) -> bool:
        """
        :param route: route to check
        :param types: possible route types
        :return: whether the route is of any of the provided types
        """
        for t in types:
            if getattr(route.path, t)():
                return True

        return False
