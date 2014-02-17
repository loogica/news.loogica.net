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

def make_text_item(title, text, owner=None):
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
    instance['comments'] = []
    return instance

class Tree(object):
    def __init__(self, name=None):
        self.name = name
        self.children = {}
        self.items = None

    def add(self, full_path, obj=None):
        path = full_path.split('/')
        name = path[0]

        if not obj:
            instance = List(full_path)
        else:
            instance = obj

        if len(path) == 1:
            tree = Tree(name)
            self.children[name] = tree
            tree.items = instance
            return instance
        else:
            if not name in self.children:
                self.children[name] = Tree(name)

            tree = self.children[name]
            tree.add(full_path.replace("{}/".format(name), ""), obj=instance)
            return instance

        return instance

    def get(self, full_path):
        path = full_path.split('/')
        name = path[0]

        if len(path) == 1:
            return self.children[name]
        else:
            tree = self.children[name]
            return tree.get(full_path.replace("{}/".format(name), ""))

    @readonly
    def has(self, full_path):
        path = full_path.split('/')
        name = path[0]

        if len(path) == 1:
            return name in self.children
        else:
            if name in self.children:
                tree = self.children[name]
                return tree.has(full_path.replace("{}/".format(name), ""))
            else:
                return False

    def add_item(self, full_path, item):
        channel = self.get(full_path).items
        channel.add(item)
        return item

    def remove_item(self, full_path, item):
        channel = self.get(full_path).items
        channel.remove(item)
        return item

    @readonly
    def find_item(self, full_path, item):
        channel = self.get(full_path).items
        return channel.find(item)

    def add_vote(self, full_path, item):
        channel = self.get(full_path).items
        return channel.vote(item)

    def add_comment(self, full_path, item, user, content):
        channel = self.get(full_path).items
        return channel.add_comment(item, user, content)

    def del_comment(self, full_path, item, comment_id):
        channel = self.get(full_path).items
        return channel.del_comment(item, user, content)

    @readonly
    def get_items(self, full_path):
        channel = self.get(full_path).items
        return channel.get_items()

    def __eq__(self, other):
        return self.name == other.name


class List(object):
    def __init__(self, name):
        self.name = name
        self.items = []
        self.index = 1

    def add(self, item):
        item['id'] = self.index
        self.items.append(item)
        self.index += 1

    def remove(self, item_id):
        self.items = list(filter(lambda x: not x['id'] == item_id, self.items))

    def find(self, item_id):
        found = list(filter(lambda x: x['id'] == item_id, self.items))[0]
        return found

    def vote(self, item_id):
        found = list(filter(lambda x: x['id'] == item_id, self.items))
        if found:
            found[0]['votes'] += 1
            return found[0]
        raise Exception("Unknow/Removed item")

    def add_comment(self, item_id, user_id, content):
        found = list(filter(lambda x: x['id'] == item_id, self.items))[0]
        comment = dict(id=len(found['comments']) + 1,user=user_id, content=content)
        found['comments'].append(comment)
        return comment

    def del_comment(self, item_id, comment_id):
        found = list(filter(lambda x: x['id'] == item_id, self.items))[0]
        comment = list(filter(lambda x: x['id'] == comment_id, found['comments']))[0]
        found['comments'].remove(comment)
        return comment

    def get_items(self):
        return sorted(self.items, key=lambda item: item['votes'], reverse=True)[:10]

    def get_user_items(self, user_id):
        return sorted(filter(lambda x: x['owner'] == user_id, self.items),
                      key=lambda item: datetime.strptime(item['posted'], DATE_FORMAT))

    def __len__(self):
        return len(self.items)
