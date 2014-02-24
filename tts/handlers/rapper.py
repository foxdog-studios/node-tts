# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


class Rapper(object):
    def __init__(self, rap_composer):
        self._rap_composer = rap_composer

    def _add_words(self, sms):
        words = sms.message.split()
        self._rap_composer.add_words(words)

    def handle(self, sms):
        rc = self._rap_composer
        if not rc.has_enough_words():
            self._add_words(sms)
            if rc.has_enough_words():
                rc.compose()
        return sms

