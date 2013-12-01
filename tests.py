import unittest

import json
import jsonq


class MockStdin(object):
    """Provides an injectable stdin-like object which can be read from."""
    def __init__(self, lines):
        self._lines = lines

    def __iter__(self):
        for line in self._lines:
            yield line


class MockStdout(object):
    """Provides an injectable stdout-like object, which we can inspect."""
    def __init__(self):
        self._buffer = []

    def write(self, some_string):
        self._buffer.append(some_string)

    def get_buffer(self):
        return self._buffer


class BaseIntegrationTestCase(unittest.TestCase):
    def query_with_input(self, input_string, query_string):
        mock_stdin = MockStdin([input_string])
        mock_stdout = MockStdout()

        # Inject the mock stdin and stdout objects into jsonq's query engine.
        jsonq.query(jsonq.parse_queries([query_string]), False, '', mock_stdin, mock_stdout)
        return mock_stdout.get_buffer()

    def query_with_expectations(self, input_string, query_string, expected_output):
        mock_stdout_buffer = self.query_with_input(input_string, query_string)

        self.assertEqual(len(expected_output), len(mock_stdout_buffer))

        for index, output in enumerate(mock_stdout_buffer):
            actual_output = json.loads(output)
            self.assertEqual(actual_output, expected_output[index])


class TestValueOperator(BaseIntegrationTestCase):
    def test(self):
        input_string = '{"key": "value"}'
        query_string = '.key'
        expected_output = ['value']

        self.query_with_expectations(input_string, query_string, expected_output)

    def test_with_nested_dicts(self):
        input_string = '{"grr": {"hello": [5, 6]}, "snafu": [{"zzz": 6}, {"aaa": 5}]}'
        query_string = '.grr.hello'
        expected_output = [[5, 6]]

        self.query_with_expectations(input_string, query_string, expected_output)



class TestListOperator(BaseIntegrationTestCase):
    def test_with_single_element_list(self):
        input_string = '["first"]'
        query_string = '[0]'
        expected_output = ['first']

        self.query_with_expectations(input_string, query_string, expected_output)

    def test_with_multi_element_list(self):
        input_string = '["first", "second", "third"]'
        query_string = '[1]'
        expected_output = ['second']

        self.query_with_expectations(input_string, query_string, expected_output)

    def test_with_list_of_dicts(self):
        input_string = '[{"derp": [1, 2, 3]}]'
        query_string = '[0].derp[1]'
        expected_output = [2]

        self.query_with_expectations(input_string, query_string, expected_output)


class TestEveryInListOperator(BaseIntegrationTestCase):
    def test_with_list_of_numbers(self):
        input_string = '[1, 2, 3]'
        query_string = '[*]'
        expected_output = [1, 2, 3]

        self.query_with_expectations(input_string, query_string, expected_output)

    def test_with_list_of_dicts(self):
        input_string = '[{"name": "jack"}, {"name": "jill"}]'
        query_string = '[*].name'
        expected_output = ['jack', 'jill']

        self.query_with_expectations(input_string, query_string, expected_output)

    def test_every_item_operator_with_nested_lists(self):
        input_string = '[["Aaron", "Amelie"], ["Brian", "Bartholomew"]]'
        query_string = '[*][*]'
        expected_output = ["Aaron", "Amelie", "Brian", "Bartholomew"]

        self.query_with_expectations(input_string, query_string, expected_output)

if __name__ == '__main__':
        unittest.main()
