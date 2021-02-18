import json
from pathlib import Path
from typing import Optional, Any


class ConfigBase:
    def __init__(self, path, name, load=False):
        self.path = path / Path(name)
        self.name = name
        self.data = {}

        if load:
            self.load()

    def put(self, key, value):
        self.data[key] = value
        self.save()

    def get(self, key) -> Optional[Any]:
        try:
            return self.data[key]
        except KeyError:
            return None

    def save(self):
        with self.path.open('w') as f:
            json.dump(self.data, f, indent=4, sort_keys=True)

    def load(self):
        try:
            with self.path.open('r') as f:
                self.data = json.load(f)

        # edit error message
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f'{self.path} - {e.msg}', e.doc, e.pos)

        # treat as empty
        except FileNotFoundError:
            pass
