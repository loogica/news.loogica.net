from coopy.decorators import readonly
from datetime import datetime, timedelta

SLICE = timedelta(minutes=30)

def Item(title, link):
    instance = {}
    instance['id'] = None
    instance['title'] = title
    instance['link'] = link
    instance['votes'] = 0
    instance['posted'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return instance

class News(object):
    def __init__(self, name):
        self.name = name
        self.items = []

    def add(self, item):
        item['id'] = len(self.items)
        self.items.append(item)

    def vote(self, item_id):
        found = filter(lambda x: x['id'] == item_id, self.items)
        if found:
            found[0]['votes'] += 1
            return found[0]
        raise Exception("Unknow/Removed item")

    def remove(self, item_id):
        self.items = filter(lambda x: not x['id'] == item_id, self.items)

    @readonly
    def get_items(self):
        return sorted(self.items, key=lambda item: item['votes'], reverse=True)

def test_news():
    import pytest
    item = Item('Loogica News', 'http://news.loogica.net')
    news = News('main')

    news.add(item)
    assert 1 == len(news.items)

    with pytest.raises(Exception):
        news.vote(10)

    assert item == news.vote(0)
    assert 1 == news.items[0]['votes']


    new_item = Item('New Video', 'http://loogica.net/videos')
    news.add(new_item)
    assert 2 == len(news.items)

    assert new_item == news.vote(1)
    assert 1 == news.items[1]['votes']
    assert new_item == news.vote(1)
    assert 2 == news.items[1]['votes']

    news.remove(0)
    assert 1 == len(news.items)
    assert 2 == news.items[0]['votes']
