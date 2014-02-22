# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import yaml


class Configuration(object):
    DEFAULT_BPM = 120

    DEFAULT_HANDLERS = {}
    DEFAULT_HANDLERS_CLEANER = None
    DEFAULT_HANDLERS_VIS_HOST = None
    DEFAULT_HANDLERS_RAPPER = True
    DEFAULT_HANDLERS_REPLY_COMPOSER = True

    DEFAULT_MELODY = '''
        r_7
                                                        B3_1/2  A3_1/2
        B3_1/2  Gb3_1/2 D3_1/2  Gb3_1/2 B2              B3_1/2  A3_1/2
        B3_1/2  Gb3_1/2 D3_1/2  Gb3_1/2 B2              B3_1/2  Db4_1/2
        D4_1/2  Db4_1/2 D4_1/2  B3_1/2  Db4_1/2 B3_1/2  Db4_1/2 A3_1/2
        B3_1/2  A3_1/2  B3_1/2  G3_1/2  B2              B3_1/2  A3_1/2
        B3_1/2  Gb3_1/2 D3_1/2  Gb3_1/2 B2              B3_1/2  A3_1/2
        B3_1/2  Gb3_1/2 D3_1/2  Gb3_1/2 B2              B3_1/2  Db4_1/2
        D4_1/2  Db4_1/2 D4_1/2  B3_1/2  Db4_1/2 B3_1/2  Db4_1/2 A3_1/2
        B3_1/2  A3_1/2  B3_1/2  Db4_1/2 D4              Gb4_1/2 E4_1/2
        Gb4_1/2 D4_1/2  A3_1/2  D4_1/2  Gb3             Gb4_1/2 E4_1/2
        Gb4_1/2 D4_1/2  A3_1/2  D4_1/2  Gb3             Gb4_1/2 Ab4_1/2
        A4_1/2  Ab4_1/2 A4_1/2  Gb4_1/2 Ab4_1/2 Gb4_1/2 Ab4_1/2 E4_1/2
        Ab4_1/2 E4_1/2  Db4_1/2 E4_1/2  Ab4             Gb4_1/2 E4_1/2
        Gb4_1/2 D4_1/2  A3_1/2  D4_1/2  Gb3             Gb4_1/2 E4_1/2
        Gb4_1/2 D4_1/2  A3_1/2  D4_1/2  Gb3             Gb4_1/2 Ab4_1/2
        A4_1/2  Ab4_1/2 A4_1/2  Gb4_1/2 Ab4_1/2 Gb4_1/2 Ab4_1/2 E4_1/2
        Ab4_1/2 E4_1/2  Db4_1/2 E4_1/2  Ab4
    '''

    DEFAULT_REPLIES = [
        'Thanks for texting in!',
    ]

    DEFAULT_SERVER = {}
    DEFAULT_SERVER_HOST = '127.0.0.1'
    DEFAULT_SERVER_PORT = 8080

    def __init__(self, path=None):
        conf = None
        if path is not None:
            with open(path) as conf_file:
                conf = yaml.load(conf_file)
        if conf is None:
            conf = {}
        self._conf = conf
        self.path = path

    @property
    def bpm(self):
        return self._conf.get('bpm', self.DEFAULT_BPM)

    @property
    def _handlers(self):
        return self._conf.get('handlers', self.DEFAULT_HANDLERS)

    @property
    def handlers_cleaner(self):
        return self._handlers.get('cleaner', self.DEFAULT_HANDLERS_CLEANER)

    @property
    def handlers_vis_host(self):
        return self._handlers.get('visHost', self.DEFAULT_HANDLERS_VIS_HOST)

    @property
    def handlers_rapper(self):
        return self._handlers.get('rapper', self.DEFAULT_HANDLERS_RAPPER)

    @property
    def handlers_reply_composer(self):
        return self._handlers.get('replyComposer',
                                  self.DEFAULT_HANDLERS_REPLY_COMPOSER)

    @property
    def melody(self):
        return self._conf.get('melody', self.DEFAULT_MELODY)

    @property
    def replies(self):
        return list(self._conf.get('replies', self.DEFAULT_REPLIES))

    @property
    def _server(self):
        return self._conf.get('server', self.DEFAULT_SERVER)

    @property
    def server_host(self):
        return self._server.get('host', self.DEFAULT_SERVER_HOST)

    @property
    def server_port(self):
        return self._server.get('port', self.DEFAULT_SERVER_PORT)

