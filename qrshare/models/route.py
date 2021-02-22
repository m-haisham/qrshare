from functools import lru_cache
from pathlib import Path
from typing import List, Union

from flask import send_file

from .zip import ZipContent


class Route:

    types = ('is_file', 'is_dir')

    def __init__(self, path, parent=None):
        self.path: Path = path
        self.parent: Route = parent
        self.sub_routes: Union[List[Route], None] = None
        self.is_root = False

    def populate(self):
        """
        :return: whether sub routes where populated this run
        """
        if not self.is_file and self.sub_routes is None:
            self.sub_routes = [Route(subdir, self) for subdir in self.path.iterdir()]
            self.sub_routes.sort(key=lambda r: (r.is_file, r.general_path()))
            return True

        return False

    def get(self):
        if self.is_file:
            return send_file(self.path)
        else:
            if self.parent:
                parent_data = self.parent.to_dict()
            else:
                parent_data = {
                    'name': '~/',
                    'path': '/',
                    'href': '/',
                    'zip': '/root.zip',
                }

            return dict(
                **self.to_dict(),
                routes=[r.to_dict() for r in self.sub_routes],
                parent=parent_data,
            )

    def zip(self):
        if self.is_file:
            return ValueError('path of type "file" cannot be zipped')
        else:
            return send_file(ZipContent(self.path.iterdir()).enclose(), mimetype='application/zip')

    @property
    def name(self):
        return self.path.name

    @property
    def is_file(self):
        return self.path.is_file()

    @lru_cache(maxsize=1024)
    def general_path(self, clean=False):
        # root?
        if self.parent is None:
            parent_route = '' if clean else '/path'
        else:
            parent_route = self.parent.general_path(clean)

        return f'{parent_route}/{self.path.name}'

    def zip_path(self):
        return f'/zip{self.general_path(clean=True).rstrip("/")}.zip'

    def to_dict(self):
        route_d = {
            'name': self.name,
            'path': self.general_path(True),
            'href': self.general_path(False),
            'isFile': self.is_file,
        }

        if not self.is_file:
            route_d.update({'zip': self.zip_path()})

        return route_d
