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

from domain import make_url_item, List, Root
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

root = Root()
users = None
if six.PY3:
    root.add('main', init_persistent_system(List('main3'), basedir="main3"))
    users = init_persistent_system(Realm('users'))
else:
    root.add('main', init_persistent_system(List('main'), basedir="main"))
    users = init_persistent_system(Realm('users3'))



@login_manager.user_loader
def load_user(userid):
    user = users.users[userid]
    return UserWrapper(userid, userid, active=True)

def authenticate(username, password):
    return users.authenticate(username, password)

@app.route('/')
def main():
    return redirect('/c/main')

@app.route('/c/<channel>')
def channel(channel):
    news = root.news[channel]
    auth = 'user_id' in session
    return render_template('loogica-news.html', channel=channel,
                                                auth=auth)

@app.route('/api/news/<channel>')
def news_channel_api(channel):
    try:
        return jsonify(channel=channel,
                    items=root.news[channel].get_items())
    except:
        return jsonify(msg="Invalid Channel")

@app.route('/api/vote/<channel>/<item_id>')
def vote_api(item_id, channel):
    item_id = int(item_id)
    news = root.news[channel]
    news.vote(item_id)
    return jsonify(channel=channel,
                   items=news.get_items())

@app.route('/api/remove/<channel>/<item_id>')
def remove_api(item_id, channel):
    item_id = int(item_id)
    news = root.news[channel]
    news.remove(item_id)
    return jsonify(items=news.get_items())

@app.route('/api/post/<channel>', methods=['POST'])
def add_api(channel):
    link = request.form['link']
    try:
        data = urlopen(link, timeout=10).read()
        if six.PY3:
            data = data.decode('utf-8')
        title_search = re.search('<title>(\n*.*\n*)</title>', data, re.IGNORECASE)
        title = title_search.group(1)
        item = make_url_item(title, link)
        news = root.news[channel]
        news.add(item)
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

@app.route('/new/<channel>')
def new_api(channel):
    return render_template('new.html', channel=channel)

@app.route('/sobre')
def about():
    return render_template('about.html')

@app.route('/recent.atom')
def recent_feed():
    feed = AtomFeed('Loogica News',
                    feed_url=request.url,
                    url=request.url_root)
    items = root.news['main'].get_items()
    for item in items:
        try:
            feed.add(title = item['title'].decode('utf-8'),
                     updated = datetime.strptime(item['posted'],
                                                   '%Y-%m-%d %H:%M:%S'),
                     url = item['link'])
        except Exception as e:
            log.debug("ewurror {0} {1}".format(e, item['title'].encode('utf-8')))

    return feed.get_response()

application = app
if __name__ == "__main__":
    app.run(debug=True)
