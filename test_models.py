from domain import Item, News, Root
from users import User, Realm

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

    root = Root()
    assert news == root.add('main', news)
    assert 'main' in root.news

def test_user():
    user = User("tester", "testerpass")
    assert user
    assert user['username'] == 'tester'

    realm = Realm('test')
    assert 0 == len(realm.users)

    realm.add_user(user)
    assert 1 == len(realm.users)
    assert True == realm.authenticate('tester', 'testerpass')
