import uuid
from functools import wraps

from flask import request, session, render_template, redirect


class Authentication:
    def __init__(self, app, code=None):
        self.app = app
        self.code = code
        self.ukey = str(uuid.uuid4())
        self.create_endpoints()

    def create_endpoints(self):

        # to prevent usage of self in wrapper
        code, ukey = self.code, self.ukey

        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                # validate submission
                if request.form['passcode'] == code:
                    session['ukey'] = ukey
                else:
                    return render_template('login.html', message='Incorrect code, Try again!', warning=True)

            # check if already authenticated
            try:
                authenticated = session['ukey'] == ukey
            except KeyError:
                authenticated = False
            finally:
                if authenticated:
                    return redirect('/')

            return render_template('login.html')

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
