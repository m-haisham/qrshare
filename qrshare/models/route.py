from pathlib import Path
from typing import List, Union
from urllib.parse import quote

from flask import send_file, render_template, Markup

from ..tools import QrTools


class Route:
    def __init__(self, path, parent=None):
        self.path: Path = path
        self.parent: Route = parent
        self.sub_routes: Union[List[Route], None] = None
        self.is_root = False

    def populate(self):
        """
        :return: whether sub routes where populated this run
        """
        if self.is_file:
            return False

        if self.sub_routes is None:
            # iterate through sub routes and add them
            # they are separated so that folders will be on top
            files = []
            dirs = []
            for subdir in self.path.iterdir():
                route = Route(subdir, self)
                if subdir.is_file():
                    files.append(route)
                else:
                    dirs.append(route)

            files.sort(key=lambda r: r.path)
            dirs.sort(key=lambda r: r.path)

            self.sub_routes = dirs + files

            return True

        return False

    def get(self):
        if self.is_file:
            return send_file(self.path)
        else:
            return render_template(
                'main.html',
                name=self.path.name,
                is_root=self.is_root,
                routes=self.sub_routes,
                parent=self.parent,
                zip=self.zip_path(),
                svg=Markup(QrTools.to_svg('asadsadas'))
            )

    def zip(self):
        if self.is_file:
            return ValueError('path of type "file" cannot be zipped')
        else:
            pass

    @property
    def name(self):
        return self.path.name

    @property
    def is_file(self):
        return self.path.is_file()

    def general_path(self):
        # root?
        if self.parent is None:
            parent_route = ''
        else:
            parent_route = self.parent.general_path()

        return quote(f'{parent_route}/{self.path.name}')

    def zip_path(self):
        return f'/zip{self.general_path().rstrip("/")}.zip'
