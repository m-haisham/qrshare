import asyncio

import tornado

from qrshare import Network, QRCode

path = 'C:/Users/User/Desktop/The Legendary Mechanic_904-921.epub'

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    app, share_url = Network.app(path, 5000)

    print(QRCode(share_url))
    print("Scan the QR code above.")
    print("Press CTRL+C to exit")

    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()

