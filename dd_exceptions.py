from dd_types import DotQuery, DotSearchable
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


class DoesNotExist(BaseException):

    """Raised when no item matching the query is found.

    If `data` is provided to init, then it will be logged.
    Not recommended for large dicts or lists.

    Requires the query to be passed in during initialization.
    """
    searchable: DotSearchable = None
    query: DotQuery = None

    def __init__(self, query: DotQuery, searchable: Optional[DotSearchable] = None):
        """Initialize the exception.

        :param DotQuery query:
            The valid query that had no matching items.
        :param DotSearchable data:
            optional, the data that was queried.
            Not recommended for large data objects.
        """
        message = f"Dictionary has no key matching query: query='{query}'"
        self.query = query
        if searchable:
            message = f"{message}, data={searchable}"
            self.searchable = searchable
        super().__init__(message)
