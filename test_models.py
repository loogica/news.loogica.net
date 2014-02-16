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

    assert item == news.vote(0)
    assert 1 == news.items[0]['votes']

    new_item = make_url_item('New Video', 'http://loogica.net/videos', owner='tester')
    news.add(new_item)
    assert 2 == len(news.items)
    assert None == news.items[0]['owner']
    assert 'tester' == news.items[1]['owner']

    assert new_item == news.vote(1)
    assert 1 == news.items[1]['votes']
    assert new_item == news.vote(1)
    assert 2 == news.items[1]['votes']

    news.remove(0)
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

    news.add_comment(0, 1, 'positive comment')
    assert 1 == len(news.items[0]['comments'])

    news.del_comment(0, 0)
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

    main = List('main')
    root.add('main', main)
    assert 1 == len(root.children)
    assert main == root.get('main').items

    specific = List('specific')
    root.add('main/specific', specific)
    assert 1 == len(root.children)
    assert 1 == len(root.children['main'].children)
    assert specific == root.get('main/specific').items

    assert Tree('specific') == root.children['main'].children['specific']
    assert Tree('specific') == root.get('main/specific')

    items = List('sub')
    root.add('main/specific/sub', items)
    assert items == root.get('main/specific/sub').items

def test_tree_list():
    root = Tree('root')

    faq = List('FAQ')
    pgto = List('PGTO')

    root.add('faq', faq)
    root.add('faq/pgto', pgto)

    item = make_text_item('Title', 'Text')
    pgto.add(item)

    assert 'Title' == root.get('faq/pgto').items.items[0]['title']

