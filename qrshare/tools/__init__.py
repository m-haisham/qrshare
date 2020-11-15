import re
from io import BytesIO
from socket import socket, AF_INET, SOCK_DGRAM

import qrcode as qr
from qrcode.image.svg import SvgPathImage


class NetworkTools:
    LOCALHOST_ADDRESS = "127.0.0.1"

    @staticmethod
    def local_ip() -> str:
        local_socket = socket(AF_INET, SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            local_socket.connect(('10.255.255.255', 1))
            ip_address = local_socket.getsockname()[0]
        except:  # noqa: E722
            ip_address = NetworkTools.LOCALHOST_ADDRESS
        finally:
            local_socket.close()

        if ip_address == NetworkTools.LOCALHOST_ADDRESS:
            raise ConnectionError(
                "Could find valid IP address for a local network. "
                "Verify that you are connected to a router.")

        return ip_address


class QrTools:
    @staticmethod
    def to_bytesio(s: str) -> BytesIO:
        handle = BytesIO()

        img = qr.make(s, image_factory=SvgPathImage)
        img.save(handle)

        return handle

    @staticmethod
    def to_svg(s: str):
        with QrTools.to_bytesio(s) as handler:
            text = handler.getvalue().decode('utf-8')

        text = re.sub(r'width=".+?"', '', text)
        text = re.sub(r'height=".+?"', '', text)

        return text