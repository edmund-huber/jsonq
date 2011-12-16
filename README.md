> echo '{"grr": {"hello": [5, 6]}, "snafu": [{"zzz": 6}, {"aaa": 5}]}' | ../devscripts/jsonq snafu[0].zzz snafu[1].aaa snafu[1].aza
6 5 null
