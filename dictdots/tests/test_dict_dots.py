import pytest
from dictdots import DictDots
from dictdots.exceptions import InvalidQueryString, DoesNotExist


@pytest.mark.parametrize("query,result", [
    ('i_should.work.1', True),
    ('1.2.3.4.5.success', True),
    ('i.should.fail\r\n', False),
    ('Ishouldpass', True),
    ('i fail', False),
    ('i.am.sneaky..snake', False),
    ('.no.beginnings', False),
    ('no.endings.', False),
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
    "please.end.me\r\n",
    "hello..world",
    ".no.beginnings",
    "no.endings.",
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
    ("under_score.bean_can.1", "found")
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
        1: "numeric key",
        "under_score": {
            "bean_can": [
                "nope",
                "found",
            ]
        }
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


@pytest.mark.parametrize("key,expected", [
    ("covenant", False),
    ("unsc.army.noble.n6", True),
    ("forerunner.warrior_servants.nice", True),
    ("covenant.banished.atriox", False),
    ("unsc", True),
    ("forerunner.warrior_servants.metarch_03", True),
])
def test_exists(key, expected):
    """Tests that ``exists`` correctly returns ``True`` when a key exists, regardless of value."""
    t = {
        "unsc": {
            "oni": {
                "director": "Parangosky",
                "section_3": {
                    "scientist": "Halsey"
                }
            },
            "army": {
                "noble": {
                    "commander": "Holland",
                    "n1": "MIA",
                    "n2": "MIA",
                    "n3": "MIA",
                    "n4": "MIA",
                    "n5": "MIA",
                    "n6": None
                }
            }
        },
        "forerunner": {
            "warrior_servants": {
                "metarch_01": "Mendicant Bias",
                "metarch_02": "Offensive Bias",
                "metarch_03": "",
                "nice": False,
            }
        },
    }
    assert DictDots.exists(t, key) == expected
