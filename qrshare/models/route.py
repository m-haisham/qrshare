import re
from pathlib import Path
from typing import List, Union
from urllib.parse import quote
from functools import lru_cache

from flask import send_file, render_template, Markup

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
                    'path': '/root',
                    'href': '/',
                    'zip': '/root.zip',
                }

            return {
                'name': self.path.name,
                'isRoot': self.is_root,
                'routes': [r.to_dict() for r in self.sub_routes],
                'parent': parent_data,
                'href': self.general_path(False, True),
                'zip': self.zip_path(),
            }

    def zip(self):
        if self.is_file:
            return ValueError('path of type "file" cannot be zipped')
        else:
            zipper = ZipContent(self.path.iterdir())
            zipper.write()
            zipper.reset_hand()

            return send_file(zipper.file, mimetype='application/zip')

    @property
    def name(self):
        return self.path.name

    @property
    def is_file(self):
        return self.path.is_file()

    @lru_cache(maxsize=4)
    def general_path(self, quoted=True, clean=False):
        # root?
        if self.parent is None:
            parent_route = '' if clean else '/path'
        else:
            parent_route = self.parent.general_path(False, clean)

        path = f'{parent_route}/{self.path.name}'
        return quote(path) if quoted else path

    def zip_path(self):
        return f'/zip{self.general_path(clean=True).rstrip("/")}.zip'

    def to_dict(self):
        return {
            'name': self.name,
            'path': self.general_path(False, False),
            'href': self.general_path(False, True),
            'isFile': self.is_file,
        }