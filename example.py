import asyncio

import tornado

from qrshare import Network, QRCode

path = 'C:/Users/User/Desktop/The Legendary Mechanic_904-921.epub'

if __name__ == '__main__':
    Network.serve(path, 5000)

