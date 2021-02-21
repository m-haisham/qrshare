import json
from typing import List, Callable, Union, Optional, Iterable

from flask import request, Response, abort

try:
    from regex import regex as re
except ImportError:
    import re

from .auth import Auth
from .models import Route

Predicate = Callable[[Route], Optional[dict]]


class Search:
    def __init__(self, app, auth: Auth):
        self.app = app
        self.auth = auth

    def create_endpoints(self):

        @self.app.app.route('/search')
        @self.auth.require_auth
        def search_point():
            # query parameters
            query = request.args.get('query')
            exts = request.args.getlist('exts')
            types = request.args.getlist('types')
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
                return abort(404)

        # remove all file routes
        return [route for route in search_routes if not route.path.is_file()]

    def create_predicate(self, query: str = None, exts: Union[str, Iterable[str]] = None,
                         types: Union[str, Iterable[str]] = None) -> Predicate:

        if not any((bool(query), bool(exts), bool(types))):
            raise ValueError('Require at least one argument (query, exts, types)')

        rx_query = None
        if query:
            # single char words would makes s... search complicated
            words = {word for word in query.split(' ') if len(word) > 1}

            rx_query = re.compile(
                '|'.join(words),
                re.IGNORECASE
            )

        rx_exts = None
        if exts:
            if type(exts) == str:
                exts = (exts,)

            # default is type iterable, any other type should be converted to iterable before this point
            # ensure extension has a dot at the start and build individual expressions
            exts = {f'(\\.{ext.lstrip(".")})(\\.|$)' for ext in exts}

            rx_exts = re.compile(
                '|'.join(exts)
            )

        # sanitizing received types
        # :throws: value error if unexpected type received
        if types:
            if type(types) == str:
                types = (types,)

            # default is type iterable, any other type should be converted to iterable before this point
            for t in types:
                if t not in Route.types:
                    raise ValueError(f'Unexpected value received: {t}; expecting {Route.types}')

            # removes any duplicate values
            types = set(types)

        def predicate(route: Route):

            # filter by path type
            # if no dir types are specified, its assumed all types are welcome
            if not self._is_route_of_type(route, types):
                return

            matches = []
            relevance = 0

            query_match = False
            exts_match = False

            # filter by query
            if rx_query is not None:
                matches += [match.regs[0] for match in rx_query.finditer(route.name)]
                query_match = True

            # filter by extension
            if rx_exts is not None and route.is_file:
                if len(route.path.suffixes) > 0:
                    matches += [match.regs[0] for match in rx_exts.finditer(route.name)]
                    exts_match = True

            # increased relevance if both query and extension match
            if query_match and exts_match:
                relevance += 1

            if matches:
                # number of matches is directly proportional to result relevance
                relevance += len(matches)

                data = route.to_dict()

                # add information relevant to search
                data.update({
                    'matches': matches,
                    'relevance': relevance,
                    'parent': route.parent.to_dict(),
                })

                return data

        return predicate

    def generator(self, routes: List[Route], predicate: Predicate, limit=200):
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

    def _is_route_of_type(self, route: Route, types: Union[List[str], None]) -> bool:
        """
        :param route: route to check
        :param types: possible route types
        :return: whether the route is of any of the provided types
        """
        # if type is an empty is or an empty string or none
        # return true, negative boolean is taken as default
        if not types:
            return True

        for t in types:
            if getattr(route.path, t)():
                return True

        return False
