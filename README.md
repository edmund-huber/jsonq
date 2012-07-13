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
query = (dict_selector | list_selector | every_in_list_selector) (query | "")
dict_selector = "." /\w+/
list_selector = "[" /\d+/ "]"
every_in_list_selector = "[*]"
````

Here are a few more examples.

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

Here are some examples using the every-in-list operator [*]:

````bash
$ echo '["Jackie", "Jason", "John"]' | ./jsonq "[*]"
"Jackie" "Jason" "John"
````

````bash
$ echo '[["Aaron", "Amelie"], ["Brian", "Bartholomew"]]' | ./jsonq "[*][*]"
"Aaron" "Amelie" "Brian" "Bartholomew"
````

Suppose we don't just want to see the result of the query, we also
want to see what was the path of selections that the query took. Use
-f/--filter:

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
