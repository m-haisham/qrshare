from pathlib import Path
from typing import List, Union
from urllib.parse import quote

from flask import send_file, render_template, Markup

from ..tools import QrTools


class Route:
    def __init__(self, qr, path, parent=None):
        self.path: Path = path
        self.parent: Route = parent
        self.sub_routes: Union[List[Route], None] = None
        self.qr = qr
        self.is_root = False

    def populate(self):
        """
        :return: whether sub routes where populated this run
        """
        if not self.is_file and self.sub_routes is None:
            self.sub_routes = [Route(self.qr, subdir, self) for subdir in self.path.iterdir()]
            self.sub_routes.sort(key=lambda r: (r.is_file, r.general_path()))
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
                svg=Markup(self.qr.svg),
                local_link=str(self.qr)
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

    def general_path(self, quoted=True):
        # root?
        if self.parent is None:
            parent_route = ''
        else:
            parent_route = self.parent.general_path()

        path = f'{parent_route}/{self.path.name}'
        return quote(path) if quoted else path

    def zip_path(self):
        return f'/zip{self.general_path().rstrip("/")}.zip'
