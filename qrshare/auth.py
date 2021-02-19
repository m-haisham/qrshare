import uuid
from functools import wraps

from flask import session, redirect, send_from_directory, request


class Auth:
    def __init__(self, app, code=None):
        self.app = app
        self.code = code
        self.ukey = str(uuid.uuid4())

    def create_endpoints(self):

        # to prevent usage of self in wrapper
        code, ukey = self.code, self.ukey

        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                # validate submission
                if request.args.get('key') == code:
                    session['ukey'] = ukey
                else:
                    return {'msg': 'The key does not match, try again.'}

            # check if already authenticated
            try:
                authenticated = not(code and session['ukey'] != ukey)
            except KeyError:
                authenticated = False

            if authenticated:
                return redirect('/')

            return send_from_directory('client/public', 'login.html')

        @self.app.route('/logout', methods=['POST'])
        def logout():
            # revoke authenticated status
            session['ukey'] = ''

            return redirect('/login')

    def require_auth(self, func):

        # to prevent usage of self in wrapper
        code, ukey = self.code, self.ukey

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                authenticated = not code or session['ukey'] == ukey
            except KeyError:
                authenticated = False

            if authenticated:
                return func(*args, **kwargs)
            else:
                return redirect('/login')

        return wrapper
