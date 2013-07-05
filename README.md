`jsonq` - a concise, self-contained library to query line-delimited JSON

What is it?
===========

Suppose you have newline-separated JSON blobs in a file. Filter down this data to what you want!

````bash
$ echo '
> {
>   "age": 22,
>   "weightLbs": 175,
>   "name": {
>     "first": "John",
>     "last": "Doe"
>   }
> }
> ' | ./jsonq .name.first
"John"
````

Query language
==============

A query is a chain of operators.

For the short of patience, here is the grammar.

````
query = (dict_operator | list_operator | every_in_list_operator) (query | "")
dict_operator = "." /\w+/
list_operator = "[" /\d+/ "]"
every_in_list_operator = "[*]"
````

The value operator `.`
----------------------

Given an object, `.key` filters to the value of the `key` given.

````bash
$ echo '{"key": "value"}' | ./jsonq .key
"value"
````

The index operator `[]`
-----------------------

Given a list, `[index]` filters to the single value at `index`.

````bash
$ echo '["first"]' | ./jsonq [0]
"first"
````

The every-in-list operator `[*]`
--------------------------------

Given a list, `[*]` unpacks the list.

````bash
$ echo '[1, 2, 3]' | ./jsonq [*]
1 2 3
````

This operator has limited uses. But suppose each blob contains a list of structures that we're trying to boil down.

````bash
$ echo '[{"name": "jack"}, {"name": "jill"}]' | ./jsonq [*].name
"jack" "jill"
````

Useful flags
============

You can choose which delimiter to use for multiple results of the same blob with `-d` or `--delimiter`:

````bash
$ echo '[1, 2, 3]' | ./jsonq [*] --delimiter="\n"
1
2
3
````

This is currently only useful for the `[*]` operator.

Suppose we don't just want to see the result of the query, we also
want to see what was the path of selections that the query took. Use
`-f` or `--filter`:

````bash
$ echo '{"grr": {"hello": [5, 6]}, "snafu": [{"zzz": 6}, {"aaa": 5}]}' | ./jsonq .grr.hello --filter
{"grr": {"hello": [5, 6]}}
````

````bash
$ echo '{"grr": {"hello": [5, 6]}, "snafu": [{"zzz": 6}, {"aaa": 5}]}' | ./jsonq .grr.hello[0] --filter
{"grr": {"hello": [5]}}
````

````bash
$ echo '{"grr": {"hello": [5, 6]}, "snafu": [{"zzz": 6}, {"aaa": 5}]}' | ./jsonq .grr.hello[1] --filter
{"grr": {"hello": [6]}}
````

More examples
=============

Just an assortment of examples.

````bash
$ echo '{"grr": {"hello": [5, 6]}, "snafu": [{"zzz": 6}, {"aaa": 5}]}' | ./jsonq .snafu[0].zzz .snafu[1].aaa .snafu[1].aza
6 5
````

````bash
$ echo '[{"derp": [1, 2, 3]}]' | ./jsonq [0].derp[1]
2
````

````bash
$ echo '{"grr": {"hello": [5, 6]}, "snafu": [{"zzz": 6}, {"aaa": 5}]}' | ./jsonq .grr.hello
[5, 6]
````

````bash
$ echo '[["Aaron", "Amelie"], ["Brian", "Bartholomew"]]' | ./jsonq "[*][*]"
"Aaron" "Amelie" "Brian" "Bartholomew"
````
