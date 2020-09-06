from qrshare import Network

paths = [
    r'C:\Users\User\Documents\Projects\Web\share\index.html',
    r'C:\Users\User\Documents\Projects\Python\qrshare\requirements.txt'
]

if __name__ == '__main__':
    Network.serve(paths, 5000)
