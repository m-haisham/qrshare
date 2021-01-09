import re
from io import BytesIO, StringIO

import qrcode as qr
from qrcode.image.svg import SvgPathImage


class QRContainer:
    def __init__(self, s):
        self.string = s

    def to_svg(self, s):
        with BytesIO() as handle:
            # create and save to svg
            img = qr.make(s, image_factory=SvgPathImage)
            img.save(handle)

            # convert svg to html embedding script
            text = handle.getvalue().decode('utf-8')

        text = re.sub(r'width=".+?"', '', text)
        text = re.sub(r'height=".+?"', '', text)

        return text

    def to_ascii(self, s):
        with StringIO() as handle:
            code = qr.QRCode()
            code.add_data(s)
            code.print_ascii(handle)

            return handle.getvalue()

    def write(self, s, stream):
        img = qr.make(s, image_factory=SvgPathImage)
        img.save(stream)

    def __str__(self):
        return self.string