````bash
echo '{"grr": {"hello": [5, 6]}, "snafu": [{"zzz": 6}, {"aaa": 5}]}' | ./jsonq .snafu[0].zzz .snafu[1].aaa .snafu[1].aza
````

6 5 null

````bash
echo '[{"derp": [1, 2, 3]}]' | ./jsonq [0].derp[1]
````

2

````bash
echo '{"grr": {"hello": [5, 6]}, "snafu": [{"zzz": 6}, {"aaa": 5}]}' | ./jsonq .grr.hello
````

[5, 6]

Use --filter to show the path that you selected down 
----------------------------------------------------

````bash
echo '{"grr": {"hello": [5, 6]}, "snafu": [{"zzz": 6}, {"aaa": 5}]}' | ./jsonq .grr.hello --filter
````

{"grr": {"hello": [5, 6]}}

````bash
echo '{"grr": {"hello": [5, 6]}, "snafu": [{"zzz": 6}, {"aaa": 5}]}' | ./jsonq .grr.hello[0] --filter
````

{"grr": {"hello": [5]}}

````bash
echo '{"grr": {"hello": [5, 6]}, "snafu": [{"zzz": 6}, {"aaa": 5}]}' | ./jsonq .grr.hello[1] --filter
````

{"grr": {"hello": [6]}}

Use --str to coerce the result to a string instead of dumping JSON
------------------------------------------------------------------

````bash
echo '{"snarf": "narf zoop"}' | ./jsonq .snarf -s
````

narf zoop