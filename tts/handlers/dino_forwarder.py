# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


class DinoForwarder(object):
    def __init__(self, dino_client):
        self._dino_client = dino_client

    def handle(self, sms):
        self._dino_client.add_sms(sms)
        return sms

