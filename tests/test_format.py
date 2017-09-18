# vi:et:ts=4 sw=4 sts=4

""" Unittests for RegexParser """

import unittest

from pyparser.format import FormatParser, pattern


TEXT = """
Hello! I don't match anything...
Hello my name is pyparser!

Goodbye my friend!
"""


class Parser(FormatParser):
    def __init__(self):
        super(Parser, self).__init__()

        self.data = {}

    @pattern('Hello my name is {name}!')
    def name(self, results):
        self.data['name'] = results.named['name']

    @pattern('{} my friend!')
    def salutation(self, results):
        self.data['salutation'] = results.fixed[0]

    def default(self, line):
        if 'unmatched' not in self.data:
            self.data['unmatched'] = 1
        else:
            self.data['unmatched'] = self.data['unmatched'] + 1


class TestFormatParser(unittest.TestCase):
    """ Tests the format parser """

    def test_normal(self):
        data = Parser().parse(TEXT.splitlines())

        self.assertIn('name', data)
        self.assertEqual('pyparser', data['name'])

        self.assertIn('salutation', data)
        self.assertEqual('Goodbye', data['salutation'])

        self.assertIn('unmatched', data)
        self.assertEqual(1, data['unmatched'])

