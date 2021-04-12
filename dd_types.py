from typing import Dict, Any, Union, List

"""The standard query type expected by DictDots."""
DotQuery = str

"""
The standard data type expected by DictDots.
This will match constants.SEARCHABLE_TYPES.
The type needs to be defined separately because python's
``isinstanceof`` doesn't work with ``typing`` objects.
"""
DotSearchable = Union[Dict[Any, Any], List[Any]]


"""A type representing the accepted key types for getter functions."""
DotCurrentKey = Union[str, int]

"""A type representing the accepted data types for getter functions."""
DotCurrentData = DotSearchable
