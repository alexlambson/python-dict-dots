import pytest
from DictDots import DictDots, InvalidQueryString


@pytest.mark.parametrize("query,result", [
    ('i_should.work.1', True),
    ('1.2.3.4.5.success', True),
    ('i.should.fail\r\n', False),
    ('Ishouldpass', True),
    ('i fail', False),
])
def test_is_valid_query(query, result):
    assert DictDots.is_valid_query(query) == result


@pytest.mark.parametrize("query", [
    "I should fail",
    "same.with me",
    "please.end.me\r\n"
])
def test_hash_get_throws_invalid_query_exception(query):
    with pytest.raises(InvalidQueryString):
        DictDots.get([], query)


@pytest.mark.parametrize('query,result,default', [
    ('a.dot.seperated.1', None, None),
    ('hello.salute', 1, None),
    ('doints.1', True, None),
    ('i.dont.exist', None, 'defaultboy')
])
def test_dots_get_succeeds(query, result, default):
    data = {
        'hello':{
            'salute':1
        },
        'doints':{
            1:True
        }
    }
    assert DictDots.get(data, query) == result or Hash.get(data, query, default) == default

