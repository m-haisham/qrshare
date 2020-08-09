from pathlib import Path
from socket import socket, AF_INET, SOCK_DGRAM
from typing import Tuple
from urllib.parse import quote

from tornado.web import Application

from .handlers import MimedStaticFileHandler


class Network:
    LOCALHOST_ADDRESS = "127.0.0.1"

    @staticmethod
    def app(path: str, port: int) -> Tuple[Application, str]:
        local_ip = Network.local_ip()

        file = Path(path)
        share_route = f'file/{quote(file.stem)}'
        share_url = f'{local_ip}:{port}/{share_route}'

        # Create file route with appropriate path and mime type
        file_handler = (
            f'/{share_route}()', MimedStaticFileHandler, {
                "path": path,
                "mime_type": "application/octet-stream"
            }
        )

        return Application(handlers=[file_handler]), share_url

    @staticmethod
    def local_ip() -> str:
        local_socket = socket(AF_INET, SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            local_socket.connect(('10.255.255.255', 1))
            ip_address = local_socket.getsockname()[0]
        except:  # noqa: E722
            ip_address = Network.LOCALHOST_ADDRESS
        finally:
            local_socket.close()

        if ip_address == Network.LOCALHOST_ADDRESS:
            raise ConnectionError(
                "Could find valid IP address for a local network. "
                "Verify that you are connected to a router.")

        return ip_address
