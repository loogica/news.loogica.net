# -*- coding: utf-8 -*-
import re
import urllib2
from datetime import datetime, timedelta

from coopy.base import init_persistent_system
from werkzeug.contrib.atom import AtomFeed
from flask import Flask, request, redirect, render_template, jsonify, url_for

from domain import Item, News, Root

import logging
log = logging.getLogger(__name__)

app = Flask(__name__)

root = Root()
root.add('main', init_persistent_system(News('main')))

@app.route('/')
def main():
    return redirect('/c/main')

@app.route('/c/<channel>')
def channel(channel):
    news = root.news[channel]
    return render_template('loogica-news.html', channel=channel)

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
        data = urllib2.urlopen(link, timeout=10).read()
        title_search = re.search('<title>(\n*.*\n*)</title>', data, re.IGNORECASE)
        title = title_search.group(1)
        item = Item(title, link)
        news = root.news[channel]
        news.add(item)
    except Exception as e:
        log.debug(e)
        return jsonify(error="Invalid Link or urlread timeout")
    return redirect(url_for('channel', channel=channel))

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
