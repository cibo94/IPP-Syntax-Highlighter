""" Base module """

#SYN:xcibul10
from syn.regex import Regex
from syn.reformat import Reformat


class Base(object):
    """ Base class """

    def __init__(self, cli):
        self._reformat = Reformat(
            Regex(cli.format), cli.input, no_overlap=cli.no_overlap,
            escape=cli.escape, line_break=cli.line_break)
        self.flusher(cli.output)

    def flusher(self, output):
        """ writes reformated string to output """
        output.write(self._reformat.output)
