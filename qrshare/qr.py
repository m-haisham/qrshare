from io import StringIO

import qrcode as qr


class QRCode:
    def __init__(self, data):
        self.code = qr.QRCode()
        self.code.add_data(data)

    def __str__(self):
        handle = StringIO()
        self.code.print_ascii(handle)

        return handle.getvalue()
