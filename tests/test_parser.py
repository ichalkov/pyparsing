# vi:et:ts=4 sw=4 sts=4

"""
Unittests for the main pyparser.Parser class
"""

import unittest

from pyparser import Parser

from tests.utils import get_filename, parse_file


class CountingParser(Parser):
    """
    A simple parser that counts the number of lines it parsed as well as
    whether or not start and finish have been called.
    """

    def __init__(self):
        super(CountingParser, self).__init__()

        self.started = False
        self.finished = False

        self.data = 0

    def process(self, line):
        self.data += 1

    def start(self):
        self.started = True

    def finish(self):
        self.finished = True

    def reset(self):
        Parser.reset(self)

        self.started = False
        self.finished = False


class TestCountingParser(unittest.TestCase):
    """
    Just test counting of lines via a parser
    """

    def setUp(self):
        self.parser = CountingParser()

    def _parse_file(self, filename, lines):
        """
        The main method that does all of the testing
        """

        self.assertFalse(self.parser.started)
        self.assertFalse(self.parser.finished)

        ifp = open(get_filename(filename))
        parsed = self.parser.parse(ifp)
        ifp.close()

        self.assertTrue(self.parser.started)
        self.assertTrue(self.parser.finished)

        self.assertEqual(parsed, lines)

        self.parser.reset()

        self.assertFalse(self.parser.started)
        self.assertFalse(self.parser.finished)
        self.assertIsNone(self.parser.data)
        self.assertFalse(self.parser.parsing)

    def test_empty(self):
        """ Test an empty file """

        self._parse_file('empty.txt', 0)

    def test_single_line(self):
        """ Test a file with a single line """

        self._parse_file('basic_single_line.txt', 1)

    def test_multiple_lines(self):
        """ Test a file with multiple lines """

        self._parse_file('basic_multiple_lines.txt', 5)


class WhiteSpaceParser(Parser):
    """
    A simple parser that counts how many lines have leading and trailing
    whitespace.
    """

    def __init__(self, strip):
        super(WhiteSpaceParser, self).__init__(
            strip=strip,
            ignore_blanks=False
        )

        self.data = {'leading': 0, 'trailing': 0}

    def process(self, line):

        if line.lstrip() != line:
            self.data['leading'] += 1

        if line.rstrip() != line:
            self.data['trailing'] += 1


class TestWhiteSpaceParser(unittest.TestCase):
    """
    Tests that the strip function of the parser works correctly
    """

    def _test_counts(self, strip, filename, leading, trailing):
        """
        The main testing method that will check that the WhiteSpaceParser found
        the correct number of lines with leading and trailing whitespace.
        """

        data = parse_file(WhiteSpaceParser, filename, strip=strip)

        self.assertEqual(data['leading'], leading)
        self.assertEqual(data['trailing'], trailing)

    def test_no_strip_empty(self):
        """ Test the WhiteSpaceParser without stripping on an empty file """

        self._test_counts(False, 'empty.txt', 0, 0)

    def test_no_strip_single(self):
        """
        Test the WhiteSpaceParser without stripping on a file with one line
        """

        self._test_counts(False, 'whitespace_single.txt', 1, 1)

    def test_no_strip_mixed(self):
        """
        Test the WhiteSpaceParser without stripping on a file with mixed
        whitespace
        """

        self._test_counts(False, 'whitespace_mixed.txt', 3, 3)

    def test_strip_empty(self):
        """ Test the WhiteSpaceParser with stripping on an empty file """

        self._test_counts(True, 'empty.txt', 0, 0)

    def test_strip_single(self):
        """
        Test the WhiteSpaceParser with stripping on a file with one line
        """

        self._test_counts(True, 'whitespace_single.txt', 0, 0)

    def test_strip_mixed(self):
        """
        Test the WhiteSpaceParser with stripping on a file with mixed
        whitespace
        """

        self._test_counts(True, 'whitespace_mixed.txt', 0, 0)


class BlankParser(Parser):
    def __init__(self, strip):
        super(BlankParser, self).__init__(strip=strip, ignore_blanks=True)

        self.data = 0

    def process(self, line):
        if line.strip() == line:
            self.data += 1


class TestIgnoreBlanks(unittest.TestCase):
    def test_ignore_blanks(self):
        blanks = parse_file(BlankParser, 'whitespace_single.txt', strip=True)

        self.assertEqual(blanks, 0)

