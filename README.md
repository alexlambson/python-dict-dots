# Python Dict Dots

---

A way access values in nested key-value dicts using dot notation, e.g.

Before:

```python
data = None
if needle in haystack:
    if nested_needle in haystack[needle]:
        data = haystack[needle][nested_needle]

if not data:
    data = default_data
```

After:

```python
from dictdots import DictDots

data = DictDots.get(
    "needle.nested_needle", haystack, default=default_data
)
```

# How to

---

- Run `pip install DictDots`
- `from dictdots import DictDots`
- `DictDots.get("needle", haystack_dict, default=default_value)`

DictDots supports `List` and `Dict`.

For example

```python
from dictdots import DictDots
haystack = [
    {
        "needle": {
            "nested": "you found me",
        },
    },
]

value = DictDots.get(haystack, "0.needle.nested")

print(value)
```

Would output `you found me`.

A valid query string is a string of keys and/or indicies, separated by periods.
Strings can only contain alphanumeric characters, periods, and underscores.
Strings can not contain double-or-more dots.
Strings can not begin or end with a dot.
Each period in the string will tell DictDots to dig another layer into your nested data structure.
Dict dots does not hold your hand, if you give it a bad string, e.g `_hello...world`, 
then it will just raise an `InvalidQueryString`.

# Future

---

[Query Language wishlist](docs/ddql.md)
