from qrshare import Network

paths = [
    'C:/Users/User/Desktop/The Legendary Mechanic_ 0-904.epub',
    'C:/Users/User/Desktop/The Legendary Mechanic_904-921.epub',
]

if __name__ == '__main__':
    Network.serve(paths, 5000)
