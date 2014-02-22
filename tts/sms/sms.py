# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from itertools import count

from tts.utils import format_obj


class Sms(object):
    _next_id = count()

    def __init__(self, number, message, original=None):
        self.id = next(self._next_id)
        self.number = number
        self.message = message
        self.original = original

    def __str__(self):
        return format_obj('[{id}, {number}] {message}', self)

