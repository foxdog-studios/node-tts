# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from itertools import cycle

from tts.sms import SmsReply


class ReplyComposer(object):
    def __init__(self, replies):
        if not replies:
            raise ValueError('at least one reply must be given')
        self._replies = cycle(replies)

    def compose(self, sms):
        number = sms.number
        message = next(self._replies)
        return SmsReply(number, message, sms)

