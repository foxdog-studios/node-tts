# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

import cherrypy

from tts.sms import Sms

__all__ = ['start']


class Server(object):
    def __init__(self, rap_composer, reply_composer):
        self._rap_composer = rap_composer
        self._reply_composer = reply_composer

    def _add_lryics(self, sms):
        self._rap_composer.add_lryics(sms)

    def _build_sms(self, number, message):
        return Sms(number, message)

    def _compose_reply(self, sms):
        return self._reply_composer.compose(sms)

    def _log(self, template, *format_args, **format_kwargs):
        cherrypy.log(
            template.format(*format_args, **format_kwargs),
            context='SERVER',
            severity=logging.INFO,
        )

    def _log_reply(self, reply):
        self._log('Sending "{message}" to {number}', message=reply.message,
                  number=reply.number)

    def _log_sms(self, sms):
        self._log('Recieved "{message}" from {number}', message=sms.message,
                  number=sms.number)

    def _make_pod_reply(self, reply):
        return [{'number': reply.number, 'message': reply.message}]

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
        self._add_lryics(sms)
        reply = self._compose_reply(sms)
        self._log_reply(reply)
        return self._make_pod_reply(reply)


def start(config, rap_composer, reply_composer):
    cherrypy.engine.autoreload.files.add(config.path)
    cherrypy.config.update({
        'server.socket_host': config.tts_host,
        'server.socket_port': config.tts_port,
    })
    root = Server(rap_composer, reply_composer)
    cherrypy.quickstart(root=root, script_name='', config={'/': {}})

