# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


class NullHandler(object):
    def handle(self, sms):
        return sms

