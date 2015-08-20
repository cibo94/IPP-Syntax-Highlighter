""" Stack module """

#SYN:xcibul10
from copy import deepcopy


class Stack(object):
    """ Stack object """

    def __init__(self):
        self._stck = []
        self._last = 0

    def __str__(self):
        out = ""
        for stuff in self._stck:
            out += " " + str(stuff)
        return out + "\n"

    def copy(self):
        """ Returns copy of whole stack object """
        return deepcopy(self)

    def clean(self):
        """ Cleans stack """
        self._last = 0

    def empty(self):
        """ Returns true if stack is empty """
        return self._last == 0

    def append(self, stck):
        """ Appends 2 stacks """
        self._last = self._last + stck._last
        self._stck = self._stck + stck._stck

    def reverse(self):
        """ Reverses stack """
        pom = []
        for ele in self._stck:
            pom.append(ele)
        self._stck = pom

    def pop(self):
        """ Pops element only from stack """
        ret = self.top()
        del self._stck[self._last-1]
        if self._last > 0:
            self._last = self._last - 1
        return ret

    def push(self, val):
        """ Push one element to stack and return itself """
        self._stck.append(deepcopy(val))
        self._last = self._last + 1
        return self

    def top(self):
        """ Returns top of a stack """
        return self._stck[self._last-1]
