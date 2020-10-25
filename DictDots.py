import re
import constants
from typing import Any
from dd_types import DotSearchable, DotQuery
from dd_exceptions import InvalidQueryString, InvalidDataType, DoesNotExist


class DictDots:
    @staticmethod
    def is_valid_query(query: DotQuery) -> bool:
        return bool(re.match(r'^[\w.]+$', query))

    @staticmethod
    def is_searchable_type(data: Any) -> bool:
        return any([isinstance(data, x) for x in constants.SEARCHABLE_TYPES])

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
    def get(searchable: DotSearchable, query: DotQuery, default: Any = None) -> Any:
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

        for key in keys:
            if key.isnumeric():
                key = int(key)
            if key in current_data:
                current_data = current_data[key]
            elif default:
                return default
            else:
                raise DoesNotExist(query)

        return current_data



