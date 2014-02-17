from datetime import datetime

from domain import make_url_item, make_text_item, List, Tree, DATE_FORMAT
from users import User, Realm

def test_news():
    import pytest
    item = make_url_item('Loogica News', 'http://news.loogica.net')
    news = List('main')

    news.add(item)
    assert 1 == len(news.items)

    with pytest.raises(Exception):
        news.vote(10)

    assert item == news.vote(1)
    assert 1 == news.items[0]['votes']

    new_item = make_url_item('New Video', 'http://loogica.net/videos', owner='tester')
    news.add(new_item)
    assert 2 == len(news.items)
    assert None == news.items[0]['owner']
    assert 'tester' == news.items[1]['owner']

    assert new_item == news.vote(2)
    assert 1 == news.items[1]['votes']
    assert new_item == news.vote(2)
    assert 2 == news.items[1]['votes']

    news.remove(1)
    assert 1 == len(news.items)
    assert 2 == news.items[0]['votes']

    for i in range(20):
        new_item = make_url_item('New Video', 'http://loogica.net/videos')
        news.add(new_item)

    assert 10 == len(news.get_items())

    new_item = make_url_item('New Video', 'http://loogica.net/videos', owner='tester')
    news.add(new_item)

    user_data = news.get_user_items('tester')
    assert 2 == len(user_data)
    d1 = datetime.strptime(user_data[0]['posted'], DATE_FORMAT)
    d2 = datetime.strptime(user_data[1]['posted'], DATE_FORMAT)
    assert d1 < d2

    root = Tree()
    assert news == root.add('main', news)
    assert 'main' in root.children

def test_news_comments():
    item = make_url_item('Loogica News', 'http://news.loogica.net')
    news = List('main')

    news.add(item)
    assert 1 == len(news.items)
    assert 0 == len(news.items[0]['comments'])

    news.add_comment(1, 1, 'positive comment')
    assert 1 == len(news.items[0]['comments'])

    news.del_comment(1, 1)
    assert 0 == len(news.items[0]['comments'])

def test_user():
    user = User("tester", "testerpass")
    assert user
    assert 'tester' == user['username']
    assert {} == user['profile']

    realm = Realm('test')
    assert 0 == len(realm.users)

    realm.add_user(user)
    assert 1 == len(realm.users)
    assert True == realm.authenticate('tester', 'testerpass')

def test_tree():
    root = Tree('root')

    assert 0 == len(root.children)
    assert 'root' == root.name

    root.add('main')
    assert 1 == len(root.children)

    root.add('main/specific')
    assert 1 == len(root.children)
    assert 1 == len(root.children['main'].children)

    assert Tree('specific') == root.children['main'].children['specific']
    assert Tree('specific') == root.get('main/specific')

    root.add('main/specific/sub')
    assert isinstance(root.get('main/specific/sub').items, List)

def test_tree_list():
    root = Tree('root')
    root.add('faq')
    root.add('faq/pgto')

    item = make_text_item('Title', 'Text')
    root.add_item('faq/pgto', item)

    assert 'Title' == root.get('faq/pgto').items.items[0]['title']

