from tornado.web import StaticFileHandler


class MimedStaticFileHandler(StaticFileHandler):
    def initialize(self, path, mime_type):
        super().initialize(path)
        self.mime_type = mime_type

    def set_extra_headers(self, path):
        self.set_header("Content-Type", self.mime_type)
