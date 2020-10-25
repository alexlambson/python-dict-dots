import pytest
from DictDots import DictDots
from dd_exceptions import InvalidQueryString, DoesNotExist


@pytest.mark.parametrize("query,result", [
    ('i_should.work.1', True),
    ('1.2.3.4.5.success', True),
    ('i.should.fail\r\n', False),
    ('Ishouldpass', True),
    ('i fail', False),
])
def test_is_valid_query(query, result):
    assert DictDots.is_valid_query(query) == result


@pytest.mark.parametrize("data,expected", [
    ({}, True),
    ([], False),
    (1, False),
    (1.0, False),
    ("hi", False),
    ({"hello", }, False),  # set
])
def test_is_searchable_type(data, expected):
    """Test that is_searchable_type only allows supported types."""
    assert DictDots.is_searchable_type(data) == expected


@pytest.mark.parametrize("query", [
    "I should fail",
    "same.with me",
    "please.end.me\r\n"
])
def test_hash_get_throws_invalid_query_exception(query):
    with pytest.raises(InvalidQueryString):
        DictDots.get({}, query)


@pytest.mark.parametrize('query,result', [
    ('hello.salute', 1),
    ('doints.1', True),
    ('hello', {'salute': 1}),
    ('doints', {1: True}),
])
def test_dots_get_succeeds__no_default(query, result):
    data = {
        'hello': {
            'salute': 1
        },
        'doints': {
            1: True,
        }
    }
    assert DictDots.get(data, query) == result


@pytest.mark.parametrize('query,default', [
    ('a.dot.seperated.1', 'test'),
    ('i.dont.exist', 'defaultboy')
])
def test_dots_get_succeeds__default(query, default):
    data = {
        'hello': {
            'salute': 1
        },
        'doints': {
            1: True,
        }
    }
    assert DictDots.get(data, query, default) == default


@pytest.mark.parametrize("query", [
    "a.b.c.1",
    "sierra.117",
    "0",
])
def test_get__raises_does_not_exist(query):
    data = {"hello": "world"}
    with pytest.raises(DoesNotExist):
        DictDots.get(data, query)
