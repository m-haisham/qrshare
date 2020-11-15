from pathlib import Path
from typing import List

import waitress
from flask import Flask, render_template
from markupsafe import Markup

from .tools import QrTools

class App:
    def __init__(self, paths: List[Path]):
        self.app = Flask(__name__)
        self.paths = paths

    def create_home(self):

        @self.app.route('/')
        def home():
            return render_template('main.html', svg=Markup(QrTools.to_svg('asadsadas')))

    def create_path(self):
        pass

    def serve(self, debug=False):
        self.create_home()

        if debug:
            self.app.run()
        else:
            waitress.serve(self.app, _quiet=True)