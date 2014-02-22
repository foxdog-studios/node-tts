# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from itertools import count


class SMS(object):
    _next_id = count()

    def __init__(self, number, message):
        self.id = next(self._next_id)
        self.number = number
        self.message = message

    def __str__(self):
        return '[{id}, {number}] {message}'.format(self)

