import hashlib

sha1 = lambda p: hashlib.sha1(p).hexdigest()

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

def test_user():
    user = User("tester", "testerpass")
    assert user
    assert user['username'] == 'tester'

    realm = Realm('test')
    assert 0 == len(realm.users)

    realm.add_user(user)
    assert 1 == len(realm.users)
    assert True == realm.authenticate('tester', 'testerpass')
