""" Regex module """

import re
from sys import stderr
from sys import exit
#SYN:xcibul10


class Regex(object):
    """ Converted regex class """

    # Extented escapes #
    escapes = [
        [r'<', r'&lt;'],
        [r'>', r'&gt;'],
        [r'&', r'&amp;']
    ]

    rules = [
        # Special characters #
        [r'(?<!%)([\\\[\]\^\$\{\}\?])', r'\\\1'],
        # NQS #
        [r'\++', r'+'],
        [r'\*+\++\**', r'*'],
        [r'\**\++\*+', r'*'],
        [r'\*+', r'*'],
        # Concateration #
        [r'([^\.])\.([^\.])', r'\1\2'],
        # negation #
        [r'!(\%.|.)', r'[^\1]'],
        # convert escapes #
        [r'%([\.\|\!\*\+\(\)\%\\])', r'\\\1'],
        # Converting basic regulars #
        [r'\%s', r'\\s'],
        [r'\%a', r'.'],
        [r'\%d', r'\\d'],
        [r'\%l', r'[a-z]'],
        [r'\%L', r'[A-Z]'],
        [r'\%w', r'[a-zA-Z]'],
        [r'\%W', r'[a-zA-Z0-9]'],
        [r'\%t', r'\\t'],
        [r'\%n', r'\\n'],
        [r'((?<!\.)\.(?!\.\*)|[^\.])', r'\1']
    ]

    # Converting format tags to html tags #
    tags = [
        [r'italic', r'i'],
        [r'bold', r'b'],
        [r'underline', r'u'],
        [r'teletype', r'tt'],
        [r'size\s*:\s*([1-7])', r'font size=\1'],
        [r'color\s*:\s*([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})', r'font color=#\1']
    ]

    def __init__(self, frmt):
        """ Constructor opens format file and read it into __file """
        self.__exp = re.compile(r"([^\t]+)\t+([^\t]+.*)")
        self.__compiled = []
        self.compile(frmt)

    def compile(self, fil):
        """ Converts format file to our array of pairs [regular ex., tag] """
        line = fil.readline()
        line_no = 0
        while line:
            line_no += 1
            res = self.__exp.match(line)
            if not res or res.group(0) != line:
                print("Chybny format vstupneho formatovacieho suboru\n" +
                      str(line_no) + ": >>> " + line, file=stderr)
                exit(4)
            reg = self.__rewrite_reg(res.group(1), line_no)
            for tag in self.__rewrite_html(res.group(2), line_no):
                self.__compiled.append([reg, tag])
            line = fil.readline()

    def __rewrite_reg(self, reg, line):
        """ Rewrites regular expression by 'rules'
            defined in this class as dictionary """
        out = reg
        reg_valid = "("
        for rule, _ in self.rules:
            reg_valid += rule + "|"
        reg_valid = reg_valid[:-1] + ")*"
        if re.match(reg_valid, reg).group(0) != out:
            print("Chybny format vstupneho formatovacieho suboru\n" +
                  str(line) + ": >>> " + reg, file=stderr)
            exit(4)
        for i in self.rules:
            out = re.sub(i[0], i[1], out)
        return out

    def __rewrite_html(self, tags, line):
        """ Rewrites tags that will be inserted into input file """
        out = tags
        html_valid = r"italic|bold|underline|teletype|size\s*:\s*([1-7])|color\s*:\s*([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})"
        if not re.match(html_valid+r"(\s*,\s*" + html_valid + r")*", tags):
            print("Chybny format vstupneho formatovacieho suboru\n" +
                  str(line) + ": >>> " + tags, file=stderr)
            exit(4)
        for tag in self.tags:
            out = re.sub(tag[0], tag[1], out)
        out = re.sub(r"\n", r"", out)
        return re.split(r"\s*,\s*", out)

    @property
    def compiled(self):
        """ Returns ompiled regular expression """
        return self.__compiled
