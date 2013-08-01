import hashlib
from flask.ext.login import UserMixin

sha1 = lambda p: hashlib.sha1(p).hexdigest()

class UserWrapper(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = name
        self.active = active

    def is_active(self):
        # Here you should write whatever the code is
        # that checks the database if your user is active
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

def User(username, password):
    return dict(username=username, password=sha1(password))

class Realm(object):
    def __init__(self, name):
        self.name = name
        self.users = {}

    def add_user(self, user):
        username = user['username']
        password = user['password']
        self.users[username] = user
        return user

    def authenticate(self, username, password):
        if not username in self.users:
            return None
        realm_user = self.users[username]
        if realm_user['password'] == sha1(password):
            return True
        return False
