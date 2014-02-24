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

    def add_rap(self, rap_path, lyrics):
        with open(rap_path, 'rb') as rap_file:
            rap = rap_file.read()
        rap = rap.encode('base64')
        rap = rap.replace('\n', '')
        rap = 'data:audio/wav;base64,{}'.format(rap)
        self._ddp.method('addRap', [rap, lyrics])

    def add_sms(self, sms):
        self._ddp.method('addSms', [sms.number, sms.message])

    def reset(self, num_words):
        self._ddp.method('reset', [num_words])

