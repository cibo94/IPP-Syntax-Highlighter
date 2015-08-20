""" Reformats input with regular expression """

#SYN:xcibul10
import re
from syn.regex import Regex
from syn.stack import Stack


class Reformat(object):
    """ Reformats input with regular expression """

    # for checking if we are replacing or inserting #
    # (escapes will replace normal chars) #
    escape = {
        r'&lt;': False,
        r'>': False,
        r'&': False,
    }

    def __init__(
            self, regex, inp, escape=False,
            line_break=False, no_overlap=False):
        """ Constructor opens file with input source
            and get compiled regular expression """
        tmp = inp.read()
        self.__escape = escape
        self.__line_break = line_break
        self.__no_overlap = no_overlap
        self.__output = self._reformat(regex.compiled, tmp)
        if self.__line_break:
            self.__output = re.sub(r"\n", r"<br />\n", self.__output)

    def _reformat(self, regulars, text):
        """ Reformats input file readed in s with regular expression reg """

        def end_tag(tag):
            """ Converts tag (in form: font color:#FFFFFF)
                to endTag </font> """
            return "</" + re.split(" ", tag)[0] + ">"

        def beg_tag(tag):
            """ Converts tag (in form: font color:#FFFFFF)
                to tag <font color=#FFFFFF> """
            return "<" + tag + ">"

        indexes = []
        counter = 0
        ident = 0
        for reg in regulars:
            m_counter = 0
            matches = re.finditer(reg[0], text, re.MULTILINE | re.DOTALL)
            for match in matches:
                if match.start() == match.end():
                    continue
                indexes.append(
                    [match.start(), beg_tag(reg[1]),
                     counter, m_counter, ident])
                indexes.append(
                    [match.end(), end_tag(reg[1]),
                     -counter, -m_counter, ident])
                m_counter += 1
                ident += 1
            counter += 1
        return self._insert(
            self._sort_merge(
                indexes,
                self._get_escape(
                    text)),
            text)

    def _get_escape(self, text):
        """ Gets position of characters that have to be escaped """
        escapes = []
        if self.__escape:
            for reg in Regex.escapes:
                matches = re.finditer(reg[0], text)
                for match in matches:
                    escapes.append([match.start(), reg[1], 0, 0])
        return escapes

    def _insert(self, inserts, text):
        """ Inserts stuffs to position in array ins """
        for ins in inserts:
            try:
                if self.escape[ins[1]]:
                    raise KeyError()
                text = text[:(ins[0])] + ins[1] + text[(ins[0]+1):]
            except KeyError:
                text = text[:(ins[0])] + ins[1] + text[(ins[0]):]
            except IndexError:
                text = text[:(ins[0])] + ins[1]
        return text

    def _remove_overlaps(self, inserts):
        """ Changes overlaps:
        <i>abab<b>ab</i>A</b>
        <i>abab</i><b><i>ab</i>A</b> """

        def _is_end_tag(tag):
            """ If tag is endtag """
            return tag[1] == '/'

        def _beg_to_end(tag):
            """ converts tag to endtag """
            return re.sub(r"<(\S*).*>", r"</\1>", tag)

        if self.__no_overlap:
            additions = []
            tags = Stack()
            i = 1
            last_line = 0
            ins_len = len(inserts)
            for ins in inserts:
                print(ins)
                if not _is_end_tag(ins[1]):
#                    print("Push: ", ins)
                    tags.push(ins)
                else:
                    if tags.top()[4] == ins[4]:
#                        print("Pop:  ", ins)
                        tags.pop()
                        continue
                    cntr = 1
                    rest = Stack()
                    while (not tags.empty()) and \
                            tags.top()[4] != ins[4] and \
                            last_line != ins[0]:
                        to_ins = tags.pop()
                        rest.push(to_ins)
                        if i != ins_len:
                            additions.append([ins[0], to_ins[1],
                                              ins[2]+cntr, to_ins[3],
                                              to_ins[4]])
                        additions.append([ins[0], _beg_to_end(to_ins[1]),
                                          ins[2]-cntr, to_ins[3], to_ins[4]])
                        cntr += 1
                    last_line = ins[0]
                    if (not tags.empty()) and tags.top()[4] == ins[4]:
                        tags.pop()
                    rest.reverse()
                    tags.append(rest)
                i += 1
            return inserts + additions
        else:
            return inserts

    def _sort_merge(self, inserts, escapes):
        """ Sorts and merge insert indexes and escape indexes """
        return sorted(
            self._remove_overlaps(
                sorted(inserts, key=lambda x: (x[0], x[2], x[3]))) +
            escapes,
            key=lambda x: (x[0], x[2], x[3]), reverse=True)

    @property
    def output(self):
        """ Returns reformated input (output) """
        return self.__output
