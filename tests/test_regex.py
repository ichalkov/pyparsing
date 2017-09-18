# vi:et:ts=4 sw=4 sts=4

""" Unittests for RegexParser """

import unittest

from pyparser.regex import RegexParser, pattern

from tests import utils


class InvalidRegexPatternTest(unittest.TestCase):
    """
    Tests that we don't raise an exception on a bad regex but instead output
    to the log.
    """

    class InvalidRegexParser(RegexParser):
        """ A parser that has an invalid regular expression decorator """
        def __init__(self, handle_errors):
            super(InvalidRegexPatternTest.InvalidRegexParser, self).__init__(
                self,
                handle_errors=handle_errors
            )

        @pattern('(')
        def _broken(self):
            """ An invalid regex pattern function """
            pass

    def test_no_error_handling(self):
        """
        Tests that an exception is raised with a bad regex and no error
        handling
        """

        with self.assertRaises(Exception):
            InvalidRegexPatternTest.InvalidRegexParser(False)

    def test_error_handling(self):
        """
        Tests that an exception is not raised with a bad regex and error
        handling
        """

        InvalidRegexPatternTest.InvalidRegexParser(True)


class CPUInfoKWArgsParser(RegexParser):
    """ Parsers /proc/cpuinfo with kwargs """

    def __init__(self):
        super(CPUInfoKWArgsParser, self).__init__(self, named_groups=True)

        self.data = {}
        self.processor = None

    @pattern('^(?P<attribute>.+[^\\s])\\s+:\\s+(?P<value>.+)$')
    def attribute(self, match, attribute, value):
        """ Parsers an attribute """

        if attribute == 'processor':
            self.processor = {}
            self.data[value] = self.processor
        else:
            if self.processor is not None:
                self.processor[attribute] = value


class CPUInfoMatchParser(RegexParser):
    """ Parsers /proc/cpuinfo without kwargs """

    def __init__(self):
        super(CPUInfoMatchParser, self).__init__()

        self.data = {}
        self.processor = None

    @pattern('^(?P<attribute>.+[^\s])\s+:\s+(?P<value>.+)$')
    def attribute(self, match):
        """ Parsers an attribute """

        if match.group('attribute') == 'processor':
            self.processor = {}
            self.data[match.group('value')] = self.processor
        else:
            if self.processor is not None:
                self.processor[match.group('attribute')] = match.group('value')


class TestRegexParser(unittest.TestCase):
    """ Tests the regex parser """

    def _test_cpu_info(self, parser):
        """ Tests the parsing of /proc/cpuinfo """
        data = utils.parse_file(parser, 'cpuinfo.txt')

        self.assertEqual(len(data), 6)

        compare = None
        for processor in data.values():
            # remove values that are volatile
            del processor['initial apicid']
            del processor['apicid']
            del processor['cpu MHz']
            del processor['bogomips']
            del processor['core id']

            if compare is None:
                compare = processor
                continue

            self.assertDictEqual(processor, compare)

    def test_cpu_info_kwargs_parser(self):
        """ Test parsing /proc/cpuinfo with kwargs """

        self._test_cpu_info(CPUInfoKWArgsParser)

    def test_cpu_info_match_parser(self):
        """ Test parsing /proc/cpuinfo without kwargs """

        self._test_cpu_info(CPUInfoMatchParser)

