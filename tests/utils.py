# vi:et:ts=4 sw=4 sts=4

"""
Some helper methods for unittesting
"""

import os


def get_filename(filename):
    """
    Gets the full filename for a data reference file
    """

    return os.path.join(os.path.dirname(__file__), 'data', filename)


def parse_file(parser, filename, *args, **kwargs):
    """
    Given a parser and a filename, will open the file, create an instance of
    parser, and parse the file with the parser and return the data.
    """

    with open(get_filename(filename)) as ifp:
        return parser(*args, **kwargs).parse(ifp)

