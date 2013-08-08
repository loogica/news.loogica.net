import pytz

from coopy.decorators import readonly
from datetime import datetime, timedelta

SLICE = timedelta(minutes=30)
DATE_FORMAT = '%Y-%m-%d %H:%M:%S %f %Z'

def make_url_item(title, link, owner=None):
    item = {
        'title': title,
        'url': link
    }
    return make_item(title, item, owner=owner)

def make_text_item(title, text):
    item = {
        'text': text,
        'title': title
    }
    return make_item(title, item, owner=owner)

def make_item(title, item, owner=None):
    instance = {}
    instance['id'] = None
    instance['title'] = title
    instance['item'] = item
    instance['votes'] = 0
    utc_date = pytz.utc.localize(datetime.now())
    instance['posted'] = utc_date.strftime(DATE_FORMAT)
    instance['owner'] = owner
    return instance

class Root(object):
    def __init__(self):
        self.news = {}

    def add(self, name, instance):
        self.news[name] = instance
        return instance

class List(object):
    def __init__(self, name):
        self.name = name
        self.items = []
        self.index = 0

    def add(self, item):
        item['id'] = self.index
        self.items.append(item)
        self.index += 1

    def vote(self, item_id):
        found = list(filter(lambda x: x['id'] == item_id, self.items))
        if found:
            found[0]['votes'] += 1
            return found[0]
        raise Exception("Unknow/Removed item")

    def remove(self, item_id):
        self.items = list(filter(lambda x: not x['id'] == item_id, self.items))

    @readonly
    def get_items(self):
        return sorted(self.items, key=lambda item: item['votes'], reverse=True)[:10]

    @readonly
    def get_user_items(self, user_id):
        return sorted(filter(lambda x: x['owner'] == user_id, self.items),
                      key=lambda item: datetime.strptime(item['posted'], DATE_FORMAT))

