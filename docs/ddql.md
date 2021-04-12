# Potential data language

This is a wishlist of how I want the query language to look.
The only things on here that work right now are `get s` and `get ns`.

I haven't yet decided if I actually want to support sets due to how
the indexing works through a hash. It would be cumbersome to try and
pass a big value into dictdots in the query string. 
## Get

Get returns a specific object matching an exact query.

-   `s` match a specific key,
    e.g. `hello.goodbye` would get `"world"` from: 
    ```python
    {
        "hello": {
            "goodbye": "world"
        },
    }
    ```
-   `n` match specific index in a list.
    e.g. `0.hello` would get `"world"` from:
    ```python
    [
        {"hello": "world"},
    ]
    ```
-   `n` match an integer key.
    e.g. `1.2` would get `"why are you using int keys?"` from:
    ```python
    {
        1: {
            2: "why are you using int keys?",
        },   
    }
    ```
-   `nfn` match a float key `n.n`,
    e.g. `100f04` gets `"e"` from `{100.04: "e"}`.
-   `ns` match a numeric string `n`, 
    e.g. `100s` would get `"e"` from `{"100": "e"}`.
-   `{s}` match a specific index in a set.
    e.g. `{hello}` would get "hello" from `{"hello", "world"}`.
    This seems somewhat useless. 

## Filter

Filter returns a list of objects that matched the query 
and an empty list if there were no matches.

Supports all `get` query args.

-   `[]` means match any index in a list. 
    Return any objects in list that match the query after the `[]`.
    e.g. `[].foo` would get `["t", "bar"]` from:
    ```python
    [
        {"foo": "t"},
        {"foo": "bar"},
        {"no": "match"},
    ]
    ```
-   `{}` match any key in a dictionary.
    Return any values that match the query after the `{{}}`.
    e.g. `{}.sierra` would get `["117", "034"]` from:
    ```python
    {
        "hello": {"sierra": "117"},
        "goodbye": {"sierra": "034"},
        "morning": {"no": "match"},
    }
    ```
-   `{,}` match any index in a set.
    Return a set of values that match the query after the `{{s}}`.
    e.g. `{,}.sierra` would get `[117, ]` from:
    ```python
    {
        {"sierra": 117},
        {"the fall of": "reach"},
    }
    ```
