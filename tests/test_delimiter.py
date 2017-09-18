# vi:et:ts=4 sw=4 sts=4

import unittest

from pyparser.delimiter import DelimiterParser


class TokenParser(DelimiterParser):
    def __init__(self, tokens=None):
        super(TokenParser, self).__init__(delimiter='|')

        self.data = []

    def process_line(self, *splits):
        self.data.append(len(splits))


class TestTokenParser(unittest.TestCase):
    def setUp(self):
        self.parser = TokenParser()

    def tearDown(self):
        self.parser = None

    def _test(self, iterable, tokens):
        data = self.parser.parse(iterable)

        self.assertListEqual(tokens, data)

    def test_emptry_string(self):
        empty = []

        self._test(empty, [])

    def test_single_line(self):
        data = ["one|two"]

        self._test(data, [2])

