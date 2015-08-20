""" Command line module """

#SYN:xcibul10
import argparse
import sys


class Cli(object):
    """ Command line parser """

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Syntax Highlighter',
            prog='syn.py')
        parser.add_argument(
            '--input', dest='input',
            help='Sets input file (if not set stdin is used)',
            metavar='FILE', default=sys.stdin, type=self.OpenFile('r'))
        parser.add_argument(
            '--format', dest='format', help='Sets format file',
            metavar='FILE', required=True, type=self.OpenFile('r'))
        parser.add_argument(
            '--output', dest='output',
            help='Sets output file (if not set stdin is used)',
            metavar='FILE', default=sys.stdout, type=self.OpenFile('w'))
        parser.add_argument(
            '--nooverlap', dest='no_overlap', action='store_true',
            default=False, help='Removes overlaps')
        parser.add_argument(
            '--escape', dest='escape', action='store_true',
            default=False, help='Escapes special characters')
        parser.add_argument(
            '--br', dest='line_break', action='store_true',
            default=False, help='Inserts <br /> before new line')
        try:
            self._arguments = parser.parse_args()
        except SystemExit as se:
            if se.code == 1:
                sys.exit(2)
            elif se.code == 2:
                sys.exit(1)
            else:
                sys.exit(se.code)

    def OpenFile(self, rw):
        """ Wrapps function that opens file for read/write """
        def _open(path):
            try:
                out = open(path, rw)
                return out
            except IOError as ex:
                print(ex, file=sys.stderr)
                if rw == "w" or ex.errno == 13:
                    sys.exit(3)
                else:
                    sys.exit(1)
        return _open

    @property
    def format(self):
        """ Returns format file name """
        return self._arguments.format

    @property
    def input(self):
        """ Returns input file name """
        return self._arguments.input

    @property
    def output(self):
        """ Returns output file name """
        return self._arguments.output

    @property
    def no_overlap(self):
        """ Remove overlaps? """
        return self._arguments.no_overlap

    @property
    def escape(self):
        """ Escape special characters? """
        return self._arguments.escape

    @property
    def line_break(self):
        """ Replace \n with <br />? """
        return self._arguments.line_break
