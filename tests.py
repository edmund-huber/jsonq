import unittest

import json
import jsonq


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
        mock_stdin = [input_string]
        mock_stdout = MockStdout()

        # Inject the mock stdin and stdout objects into jsonq's query engine.
        jsonq.query(jsonq.parse_queries([query_string]), False, '', mock_stdin, mock_stdout)
        return mock_stdout.get_buffer()

    def test_query_with_expectations(self):
        # unittest has a bunch of convenient skip functions but nothing that'll allow you
        # to simply define when you want to skip an entire test suite (ie; testify's __test__)
        # class variable.
        if type(self) is BaseIntegrationTestCase:
           self.skipTest("Skipping base class.")

        mock_stdout_buffer = self.query_with_input(self.input_string, self.query_string)

        self.assertEqual(len(self.expected_output), len(mock_stdout_buffer))

        for index, output in enumerate(mock_stdout_buffer):
            actual_output = json.loads(output)
            self.assertEqual(actual_output, self.expected_output[index])


class TestValueOperator(BaseIntegrationTestCase):
    input_string = '{"key": "value"}'
    query_string = '.key'
    expected_output = ['value']


class TestValueOperatorWithNestedDicts(BaseIntegrationTestCase):
    input_string = '{"grr": {"hello": [5, 6]}, "snafu": [{"zzz": 6}, {"aaa": 5}]}'
    query_string = '.grr.hello'
    expected_output = [[5, 6]]


class TestListOperatorWithSingleElementList(BaseIntegrationTestCase):
    input_string = '["first"]'
    query_string = '[0]'
    expected_output = ['first']


class TestListOperatorWithMultiElementList(BaseIntegrationTestCase):
    input_string = '["first", "second", "third"]'
    query_string = '[1]'
    expected_output = ['second']


class TestListOperatorWithListOfDicts(BaseIntegrationTestCase):
    input_string = '[{"derp": [1, 2, 3]}]'
    query_string = '[0].derp[1]'
    expected_output = [2]


class TestEveryInListOperatorWithListOfNumbers(BaseIntegrationTestCase):
    input_string = '[1, 2, 3]'
    query_string = '[*]'
    expected_output = [1, 2, 3]


class TestEveryInListOperatorWithListOfDicts(BaseIntegrationTestCase):
    input_string = '[{"name": "jack"}, {"name": "jill"}]'
    query_string = '[*].name'
    expected_output = ['jack', 'jill']


class TestEveryInListOperatorWithNestedLists(BaseIntegrationTestCase):
    input_string = '[["Aaron", "Amelie"], ["Brian", "Bartholomew"]]'
    query_string = '[*][*]'
    expected_output = ["Aaron", "Amelie", "Brian", "Bartholomew"]


if __name__ == '__main__':
        unittest.main()
