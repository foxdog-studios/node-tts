# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

import cherrypy

from tts.sms import Sms


class Server(object):
    def __init__(self, handler):
        self._handler = handler

    def _build_sms(self, number, message):
        return Sms(number, message)

    def _handle(self, sms):
        return self._handler.handle(sms)

    def _log(self, template, *format_args, **format_kwargs):
        cherrypy.log(
            template.format(*format_args, **format_kwargs),
            context='SERVER',
            severity=logging.INFO,
        )

    def _log_reply(self, reply):
        for sms in reply:
            self._log('Sending "{message}" to {number}', message=sms.message,
                      number=sms.number)

    def _log_sms(self, sms):
        self._log('Recieved "{message}" from {number}', message=sms.message,
                  number=sms.number)

    def _to_serializable(self, reply):
        def serialisable_sms(sms):
            return {'number': sms.number, 'message': sms.message}
        return [serialisable_sms(sms) for sms in reply]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, number=None, message=None):
        if number is None or message is None:
            raise cherrypy.HTTPError(
                status=400,
                message='Either number or message to given',
            )
        sms = self._build_sms(number, message)
        self._log_sms(sms)
        reply = self._handle(sms)
        self._log_reply(reply)
        return self._to_serializable(reply)

