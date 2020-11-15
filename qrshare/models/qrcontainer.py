import re
from io import BytesIO

import qrcode as qr
from qrcode.image.svg import SvgPathImage


class QRContainer:
    def __init__(self, s):
        self.string = s
        self.svg = self._to_svg(s)

    def _to_svg(self, s):
        with BytesIO() as handle:
            # create and save to svg
            img = qr.make(s, image_factory=SvgPathImage)
            img.save(handle)

            # convert svg to html embedding script
            text = handle.getvalue().decode('utf-8')

        text = re.sub(r'width=".+?"', '', text)
        text = re.sub(r'height=".+?"', '', text)

        return text

    def __str__(self):
        return self.string