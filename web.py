# -*- coding: utf-8 -*-
import six
import re

try:
    from urllib2 import urlopen
except:
    from urllib.request import urlopen

from datetime import datetime, timedelta

from coopy.base import init_persistent_system
from flask import (Flask, request, redirect, render_template, jsonify, session,
                   url_for)
from flask.ext.login import LoginManager, login_user, logout_user
from werkzeug.contrib.atom import AtomFeed

from decouple import Config

from domain import make_text_item, List, Tree, DATE_FORMAT
from users import User, Realm, UserWrapper

import logging
log = logging.getLogger(__name__)

config = Config('settings.ini')
app = Flask(__name__)
app.secret_key = config('SECRET_KEY').encode('utf-8')
app.logger.addHandler(logging.StreamHandler())
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)

users = None
if six.PY3:
    root = init_persistent_system(Tree(), basedir="main3")
    root.add('main')
    users = init_persistent_system(Realm('users3'))
else:
    root = init_persistent_system(Tree(), basedir="main")
    root.add('main')
    users = init_persistent_system(Realm('users'))



@login_manager.user_loader
def load_user(userid):
    user = users.users[userid]
    return UserWrapper(userid, userid, active=True)

def authenticate(username, password):
    return users.authenticate(username, password)

@app.route('/')
def main():
    return redirect('/c/main')

@app.route('/c/<path:channel>')
def channel(channel):
    auth = 'user_id' in session
    return render_template('loogica-news.html', channel=channel,
                                                auth=auth)

@app.route('/item/<path:channel>/<int:pk>')
def item(channel, pk):
    item = root.get(channel).find(channel, pk)
    auth = 'user_id' in session
    return render_template('loogica-item.html', item_id=pk,
                                                item=item,
                                                channel=channel,
                                                auth=auth)

@app.route('/api/news/<path:channel>')
def news_channel_api(channel):
    try:
        return jsonify(channel=channel,
                       items=root.get_items(channel))
    except Exception as e:
        log.error(e)
        return jsonify(msg="Invalid Channel")

@app.route('/api/<path:channel>/<int:pk>')
def item_api(channel, pk):
    item = root.get(channel).find(pk)
    return jsonify(item=item)


@app.route('/api/vote/<path:channel>/<item_id>')
def vote_api(item_id, channel):
    item_id = int(item_id)
    news = root.get(channel).items
    news.vote(item_id)
    return jsonify(channel=channel,
                   items=news.get_items())

@app.route('/api/remove/<path:channel>/<item_id>')
def remove_api(item_id, channel):
    item_id = int(item_id)
    news = root.get(channel).items
    news.remove(item_id)
    return jsonify(items=news.get_items())

@app.route('/api/channel/add/<path:channel>')
def add_channel(channel):
    name = channel.split('/')[-1]
    root.add(channel, List(name))
    return jsonify(path=channel, name=name)


@app.route('/api/post/<path:channel>', methods=['POST'])
def add_api(channel):
    #import pytest; pytest.set_trace()
    #import ipdb; ipdb.set_trace()
    title = request.form['title']
    text = request.form['text']
    try:
        item = make_text_item(title, text)
        root.add_item(channel, item)
    except Exception as e:
        log.debug(e)
        return jsonify(error="Invalid Link or urlread timeout")
    return redirect(url_for('channel', channel=channel))

@app.route('/user/new')
def user_form():
    post_url = '/user/create'
    return render_template('user.new.html', post_url=post_url)

@app.route('/user/login')
def login_form():
    post_url = '/login'
    return render_template('user.new.html', post_url=post_url)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if authenticate(username, password):
        login_user(load_user(username))
    return redirect('/')

@app.route('/user/create', methods=['POST'])
def user_create():
    username = request.form['username']
    password = request.form['password']
    if username and password:
        users.add_user(User(username, password))
        login_user(load_user(username))
    return redirect('/')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/new')
def new():
    return redirect('/new/main')

@app.route('/new/<path:channel>')
def new_api(channel):
    return render_template('new.html', channel=channel)

@app.route('/sobre')
def about():
    return render_template('about.html')

@app.route('/recent/<path:channel>/atom')
def recent_feed(channel):
    feed = AtomFeed('Loogica News',
                    feed_url=request.url,
                    url=request.url_root)
    items = root.get(channel).items.get_items()
    for item in items:
        try:
            feed.add(url = "http://{}/item/{}/{}".format(request.host, channel, item['id']),
                     title = item['title'].decode('utf-8'),
                     updated = datetime.strptime(item['posted'], DATE_FORMAT),
                     text = item['item']['text'])
        except Exception as e:
            log.debug("Error {0} {1}".format(e, item['title'].encode('utf-8')))

    return feed.get_response()

application = app
if __name__ == "__main__":
    app.run(debug=True)
