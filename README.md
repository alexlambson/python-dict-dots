# Python Dict Dots
A way access values in nested key-value dicts using dot notation.

I wrote this is reduce the amount of times I will have to do

```
data = None
if nested_needle in haystack[needle]:
    data = haystack[needle][nested_needle]
```

or some kind of loop that searches nested dicts

[Query Language wishlist](docs/ddql.md)
