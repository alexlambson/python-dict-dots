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
    """Test that queries can be validated."""
    assert DictDots.is_valid_query(query) == result


@pytest.mark.parametrize("data,expected", [
    ({}, True),
    ([], True),
    (1, False),
    (1.0, False),
    ("hi", False),
    ({"hello", }, False),  # set
])
def test_is_searchable_type(data, expected):
    """Test that is_searchable_type only allows supported types.

    Supported types are in :data:`constants.SEARCHABLE_TYPES`
    """
    assert DictDots.is_searchable_type(data) == expected


@pytest.mark.parametrize("query", [
    "I should fail",
    "same.with me",
    "please.end.me\r\n"
])
def test_hash_get_throws_invalid_query_exception(query):
    """Tests that an error is raised for invalid queries."""
    with pytest.raises(InvalidQueryString):
        DictDots.get({}, query)


@pytest.mark.parametrize('query,result', [
    ('hello.salute', 1),
    ('doints.1', True),
    ('hello', {'salute': 1}),
    ('doints', {1: True}),
    ("list.0", 1),
    ("1", "numeric key"),
])
def test_dots_get_succeeds__no_default(query, result):
    """Tests that get retrieves the correct value."""
    data = {
        'hello': {
            'salute': 1
        },
        'doints': {
            1: True,
        },
        "list": [
            1,
            2,
        ],
        1: "numeric key"
    }
    assert DictDots.get(data, query) == result


@pytest.mark.parametrize("query,result", [
    ("0", 1),
    ("1", 2),
    ("2", "three"),
    ("3.four.success", True),
    ("3.four", {"success": True, }),
])
def test_dots_get_succeeds__list_data(query, result):
    data = [
        1,
        2,
        "three",
        {
            "four": {
                "success": True
            }
        }
    ]
    assert DictDots.get(data, query) == result


@pytest.mark.parametrize('query,default,expected', [
    ('a.dot.seperated.1', 'test', "test"),
    ('i.dont.exist', 'defaultboy', "defaultboy"),
    ("hello.salute", "default", 1),
    ("doints.1", "d", True),
    ("hello.saluted", "d", "d"),
    ("hello", "d", {"salute": 1, })
])
def test_dots_get_succeeds__default(query, default, expected):
    """Test that the default is returned if no value found."""
    data = {
        'hello': {
            'salute': 1
        },
        'doints': {
            1: True,
        }
    }
    assert DictDots.get(data, query, default) == expected


@pytest.mark.parametrize("query", [
    "a.b.c.1",
    "sierra.117",
    "0",
])
def test_get__raises_does_not_exist(query):
    """Test that an error is raised if no data is found and no default is provided."""
    data = {"hello": "world"}
    with pytest.raises(DoesNotExist):
        DictDots.get(data, query)
