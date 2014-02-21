import json
import os
import shutil
import unittest


class NewsView(unittest.TestCase):
    def setUp(self):
        import web
        reload(web)
        self.app = web.app.test_client()

    def tearDown(self):
        try:
            shutil.rmtree('main')
        except:
            pass

    def login(self, username, password):
        return self.app.post('/login', data=dict(username=username,
                                                 password=password),
                                       follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_get_home(self):
        response = self.app.get('/', follow_redirects=True)
        assert 200 == response.status_code
        assert 'Login' in response.data
        assert 'Criar Conta' in response.data

    def test_get_main_channel(self):
        response = self.app.get('/c/main', follow_redirects=True)
        assert 200 == response.status_code
        assert 'Login' in response.data
        assert 'Criar Conta' in response.data

    def test_post_link(self):
        data = dict(title="Title", text="Specific Text")
        response = self.app.post('/api/post/main', data=data, follow_redirects=True)
        assert 200 == response.status_code
        assert 'Login' in response.data
        assert 'Criar Conta' in response.data

    def test_add_channel(self):
        response = self.app.get('/api/channel/add/main/sub')
        assert 200 == response.status_code
        assert "main/sub" in response.data

    def test_post_link_subtopic(self):
        data = dict(title="Title", text="Specific Text")
        response = self.app.get('/api/channel/add/main/sub')
        response = self.app.post('/api/post/main/sub', data=data, follow_redirects=True)
        assert 200 == response.status_code
        assert 'Login' in response.data
        assert 'Criar Conta' in response.data

    def test_get_channel_json(self):
        data = dict(title="Title", text="Specific Text")
        response = self.app.post('/api/post/main', data=data, follow_redirects=True)
        response = self.app.get('/api/news/main')
        assert 'Specific Text' in response.data

    def test_get_vote_api(self):
        data = dict(title="Title", text="Specific Text")
        response = self.app.post('/api/post/main', data=data, follow_redirects=True)
        response = self.app.get('/api/news/main')
        assert '"votes": 0' in response.data
        response = self.app.post('/api/vote/main/1', data=json.dumps(dict(vote=1)), content_type="application/json")
        assert '"votes": 1' in response.data
        response = self.app.post('/api/vote/main/1', data=json.dumps(dict(vote=-1)), content_type="application/json")
        assert not '"votes": 1' in response.data
        assert '"votes": 0' in response.data

    def test_get_remove_api(self):
        data = dict(title="Title", text="Specific Text")
        response = self.app.post('/api/post/main', data=data, follow_redirects=True)
        response = self.app.get('/api/news/main')
        assert 'Specific Text' in response.data
        response = self.app.get('/api/remove/main/1')
        assert not 'Specific Text' in response.data

    def test_get_user_form(self):
        response = self.app.get('/user/new')
        assert '/user/create' in response.data

    def test_get_login_form(self):
        response = self.app.get('/user/login')
        assert '/login' in response.data

    def test_post_user_create(self):
        data = dict(username="user", password="pass")
        response = self.app.post('/user/create', data=data, follow_redirects=True)
        assert 'Logout' in response.data

    def test_post_login(self):
        data = dict(username="user", password="pass")
        response = self.app.post('/user/create', data=data, follow_redirects=True)
        response = self.app.post('/login', data=data, follow_redirects=True)
        assert 'Logout' in response.data

    def test_post_logout(self):
        data = dict(username="user", password="pass")
        response = self.app.post('/user/create', data=data, follow_redirects=True)
        response = self.app.post('/login', data=data, follow_redirects=True)
        assert 'Logout' in response.data
        response = self.app.get('/logout', follow_redirects=True)
        assert 'Login' in response.data

    def test_feed(self):
        data = dict(link="http://loogica.net")
        response = self.app.post('/api/post/main', data=data, follow_redirects=True)
        response = self.app.get('/recent/main/atom')
        assert 'Loogica' in response.data
