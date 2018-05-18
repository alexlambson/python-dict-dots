import re


class InvalidQueryString(Exception):
    def __init__(self):
        super().__init__("Query must be a dot-notation string containing only alphanumeric characters and dots")


class DictDots:
    @staticmethod
    def is_valid_query(query):
        return bool(re.match('^[\w\.]+$', query))

    @staticmethod
    def get(data, query, default=None):
        """

        Args:
            data (dict):
            query (str):
            default:

        Returns:

        """
        if not DictDots.is_valid_query(query):
            raise InvalidQueryString

        keys = query.split('.')
        current_data = data

        for key in keys:
            if key.isnumeric():
                key = int(key)
            if key in current_data:
                current_data = current_data[key]
            else:
                return default

        return current_data



