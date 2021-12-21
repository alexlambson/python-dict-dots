from dictdots.types import DotQuery, DotSearchable
from typing import Optional, Any


class InvalidQueryString(BaseException):

    """Raised when a query doesn't match the DictDots query language."""
    invalid_query: DotQuery = None

    def __init__(self, query: DotQuery):
        """Initializes the exception.

        :param DotQuery query:
            An invalid query string.
        """
        self.invalid_query = query
        super().__init__(f"Query must match the DictDots query language: query='{query}'")


class InvalidDataType(BaseException):

    """Raised when an unsupported data type is given to DictDots."""

    def __init__(self, data: Any):
        """Initializes the exception.

        :param Any data:
            The unsupported-type object that was passed to DictDots.
        """
        super().__init__(
            f"Object passed to DictDots is not searchable: type={type(data).__name__}"
        )


class KeyNotFound(BaseException):
    key = None
    searchable = None

    def __init__(self, current_key, searchable=None):
        message = f"Key not found in data: key='{current_key}', key_type='{type(current_key)}'"
        self.key = current_key

        if searchable:
            message = f"{message}, data={searchable}"
            self.searchable = searchable

        super().__init__(message)


class DoesNotExist(BaseException):

    """Raised when no item matching the query is found.

    This exception is to be raised when a query doesn't resolve for the provided searchable data
    and if no default was provided.

    If ``data`` is provided to init, then it will be logged.
    Not recommended for large dicts or lists.

    If ``key_error`` is provided to init, then the specific key and data that caused the
    failure will be included in the log message.

    Requires the query to be passed in during initialization.
    """
    searchable: DotSearchable = None
    query: DotQuery = None

    def __init__(self, query: DotQuery, searchable: Optional[DotSearchable] = None, key_error: KeyNotFound = None):
        """Initialize the exception.

        :param DotQuery query:
            The valid query that had no matching items.
        :param DotSearchable searchable:
            optional, the data that was queried.
            Not recommended for large data objects.
        :param KeyNotFound key_error:
            optional, the error that was raised and triggered this error.
            If provided, this error's message will contain info about which specific key
            was invalid in the provided query.
        """
        message = f"Dictionary has no key matching query: query='{query}'"
        self.query = query
        if searchable:
            message = f"{message}, data={searchable}"
            self.searchable = searchable
        if key_error:
            message = f"{message}, current_key={key_error.key}, current_data={key_error.searchable}"
        super().__init__(message)
