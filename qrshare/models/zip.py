import tempfile
from pathlib import Path
from typing import List
from zipfile import ZipFile


class ZipContent:
    def __init__(self, paths):
        self.paths: List[Path] = paths
        self.file = tempfile.NamedTemporaryFile(suffix='.zip')

    def write(self):
        zipfile = ZipFile(self.file, mode='w')
        for path in self.paths:
            # files
            if path.is_file():
                zipfile.write(path, arcname=path.name)
            # folders
            else:
                for sub_path in path.rglob('*'):
                    zipfile.write(sub_path, sub_path.relative_to(path.parent))
        zipfile.close()

    def reset_hand(self):
        self.file.seek(0)

    def enclose(self):
        self.write()
        self.reset_hand()
        return self.file
