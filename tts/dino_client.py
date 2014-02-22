# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ddp.client import DdpClient


class DinoClient(object):
    def __init__(self, *args, **kwargs):
        self._ddp = DdpClient(*args, **kwargs)

    def connect(self):
        self._ddp.connect()

    def disconnect(self):
        self._ddp.disconnect()

    def add_sms(self, sms):
        self._ddp.method('addSms', [sms.number, sms.message])

    def reset(self, num_words):
        self._ddp.method('reset', [num_words])

