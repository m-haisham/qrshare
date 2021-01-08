import uuid
from functools import wraps

from flask import session, redirect, send_from_directory


class Authentication:
    def __init__(self, app, code=None):
        self.app = app
        self.code = code
        self.ukey = str(uuid.uuid4())
        self.create_endpoints()

    def create_endpoints(self):

        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            # TODO authentication logic

            return send_from_directory('client/public', 'login.html', cache_timeout=self.app.cache_timeout)

    def require_auth(self, func):

        # to prevent usage of self in wrapper
        code, ukey = self.code, self.ukey

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                authenticated = not(code and session['ukey'] != ukey)
            except KeyError:
                authenticated = False

            if authenticated:
                return func(*args, **kwargs)
            else:
                return redirect(f'/login')

        return wrapper
