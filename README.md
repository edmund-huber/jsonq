Get the information that you want out of JSON.

For example, let's say you have a file with a ton of JSON, one JSON
structure per line. Each of the JSON looks something like this:

````javascript
{
  "age": 22,
  "weightLbs": 175,
  "name": {
    "first": "John",
    "last": "Doe"
  }
}
````

You can extract a list of each person's first name using:

````bash
$ ./jsonq .name.first < info | tail -1
"John"
````

The JSON query language is pretty simple. Here is the grammar:

````
query = (dict_selector | list_selector) (query | "")
dict_selector = "." /\w+/
list_selector = "[" /\d+/ "]"
````

Here are a few more examples.

````bash
$ echo '{"grr": {"hello": [5, 6]}, "snafu": [{"zzz": 6}, {"aaa": 5}]}' | ./jsonq .snafu[0].zzz .snafu[1].aaa .snafu[1].aza
6 5 null
````

````bash
$ echo '[{"derp": [1, 2, 3]}]' | ./jsonq [0].derp[1]
2
````

````bash
$ echo '{"grr": {"hello": [5, 6]}, "snafu": [{"zzz": 6}, {"aaa": 5}]}' | ./jsonq .grr.hello
[5, 6]
````

When you don't know quote where to find what you want, use -f/--find,
which makes jsonq emit all queries which would find any of the
substrings which you have supplied. For example, suppose we're looking
for "5", or "derp", we just don't know.

````bash
$ echo '{"herp": {"derp": [5]}, "derp": [1,2,3]}' | ./jsonq -f 5 derp
for the input:  {"herp": {"derp": [5]}, "derp": [1, 2, 3]}
using query ".herp.derp[0]", jsonq would find:  5
using query ".herp", jsonq would find:  {'derp': [5]}
using query "", jsonq would find:  {'herp': {'derp': [5]}, 'derp': [1, 2, 3]}
````

Now, suppose we don't just want to see the result of the query, we
also want to see what was the path of selections that the query
took. Use -i/--filter:

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

One last thing. Use -s/--str to coerce the result to a string instead of dumping JSON.

````bash
$ echo '{"snarf": "narf zoop"}' | ./jsonq .snarf -s
narf zoop
````
