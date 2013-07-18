from coopy.base import init_persistent_system
from flask import Flask, request, redirect, render_template, jsonify, url_for

from domain import Item, News

app = Flask(__name__)
news = init_persistent_system(News('main'))

@app.route('/')
def main():
    return render_template('loogica-news.html', items=news.items)

@app.route('/api/news')
def news_api():
    return jsonify(items=news.get_items())

@app.route('/api/vote/<item_id>')
def vote_api(item_id):
    item_id = int(item_id)
    news.vote(item_id)
    return jsonify(items=news.get_items())

@app.route('/api/post', methods=['POST'])
def add_api():
    title = request.form['title']
    link = request.form['link']
    item = Item(title, link)
    news.add(item)
    return redirect(url_for('main'))

@app.route('/new')
def new():
    return render_template('new.html')

@app.route('/sobre')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
