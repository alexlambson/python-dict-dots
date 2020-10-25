from typing import Dict, Any

"""The standard query type expected by DictDots."""
DotQuery = str

"""
The standard data type expected by DictDots.
This will match constants.SEARCHABLE_TYPES.
The type needs to be defined separately because python's
`isinstanceof` doesn't work with `typing` objects.
"""
DotSearchable = Dict[Any, Any]

