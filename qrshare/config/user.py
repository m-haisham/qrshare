from pathlib import Path
from uuid import uuid4

from appdirs import user_config_dir
from .base import ConfigBase

appname = 'qrshare'
appauthor = 'mHaisham'


class UserConfig:
    def __init__(self):
        # get cross os configuration path
        self.path = Path(user_config_dir(appname, appauthor))
        self.path.mkdir(parents=True, exist_ok=True)

        self.config = ConfigBase(self.path, 'config.json', load=True)
        self.init_secret_key()

    def init_secret_key(self):
        key = self.config.get("SECRET_KEY")
        if key is None:
            self.config.put("SECRET_KEY", str(uuid4()))
