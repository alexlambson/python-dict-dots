import re
from typing import Any
from .types import DotSearchable, DotQuery, DotCurrentKey, DotCurrentData
from .exceptions import InvalidQueryString, InvalidDataType, DoesNotExist, KeyNotFound
from . import constants


class DictDots:
    @staticmethod
    def is_valid_query(query: DotQuery) -> bool:
        """Check if the query string has only valid characters.

        Queries, for the time being, only allow alphanumeric and dots ``.``

        :param DotQuery query:
            The dev-provided query string.
        :return bool:
            Whether or not this query is valid.
        """
        # alphanumeric + dots that does not begin or end with a dot.
        characters_allowed = bool(re.match(r'^(?!\.)[\w.]+(?<!\.)$', query))
        empty_keys = bool(re.search(r'\.{2,}', query))

        return characters_allowed and not empty_keys

    @staticmethod
    def is_searchable_type(data: Any) -> bool:
        """Check that the data can be searched by DictDots.

        :param Any data:
            The data the user wants to query.
        :return bool:
            Whether or not the data can be queried.
        """
        return any([isinstance(data, x) or issubclass(type(data), x) for x in constants.SEARCHABLE_TYPES])

    @staticmethod
    def _validate_get(searchable: DotSearchable, query: DotQuery) -> None:
        """Validate parameters for get.

        :param DotSearchable searchable:
            The object we're trying to dig into.
        :param DotQuery query:
            The query to search searchable for
        :raises InvalidDataType:
        :raises InvalidQueryString:
        """
        if not DictDots.is_searchable_type(searchable):
            raise InvalidDataType(searchable)

        if not DictDots.is_valid_query(query):
            raise InvalidQueryString(query)

    @staticmethod
    def _list_getter(current_key: DotCurrentKey, current_data: DotCurrentData) -> Any:
        try:
            return current_data[current_key]
        except IndexError:
            raise KeyNotFound(current_key, current_data)

    @staticmethod
    def _dict_getter(current_key: DotCurrentKey, current_data: DotCurrentData) -> Any:
        if current_key in current_data:
            return current_data[current_key]

        raise KeyNotFound(current_key, current_data)

    @classmethod
    def get(cls, searchable: DotSearchable, query: DotQuery, default: Any = None) -> Any:
        """Get a specific nested value.
        
        Args:
            searchable (DotSearchable):
            query (DotQuery):
            default (Any):
                What to return if nothing matching the query is found.
                An error will be raised if nothing is found and no default is set.

        Returns (Any):
            The result matching `query` if found.

        Raises:
            Exception: Raised if no item was found and no default was provided.
        """
        DictDots._validate_get(searchable, query)
        keys = query.split('.')
        # current_data is the value we are currently digging into.
        current_data = searchable

        type_methods = {
            dict: cls._dict_getter,
            list: cls._list_getter,
        }

        for key in keys:
            if key.isnumeric():
                # We don't support numerical strings for now, so convert them to ints.
                key = int(key)

            method = type_methods[type(current_data)]

            try:
                current_data = method(key, current_data)
            except KeyNotFound as e:
                if default:
                    return default
                raise DoesNotExist(query, searchable, e)

        return current_data



