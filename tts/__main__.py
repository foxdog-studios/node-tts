# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from argparse import ArgumentParser
from collections import OrderedDict
import logging
import sys

import ddp

from tts.swift import Swift

LOG_LEVELS = (
    logging.CRITICAL,
    logging.ERROR,
    logging.WARNING,
    logging.INFO,
    logging.DEBUG
)

LOG_LEVEL_TO_NAMES = OrderedDict((level, logging.getLevelName(level).lower())
                                 for level in LOG_LEVELS)
LOG_NAME_TO_LEVEL = OrderedDict((name, level)
                                for level, name in LOG_LEVEL_TO_NAMES.items())


class DdpClient(object):
    def __init__(self, url):
        self._conn = ddp.DdpConnection(
                url,
                received_message_callback=self._received_message)
        self._swift = Swift()
        self._next_id = 1

    def _get_next_id(self):
        id_ = self._next_id
        self._next_id += 1
        return str(id_)

    def _handle_added(self, message):
        fields = message.fields
        id_ = message.id_
        ssml = message.fields[u'ssml']
        self._render(id_, ssml)

    def _received_message(self, message):
        print(message)
        if isinstance(message, ddp.AddedMessage):
            self._handle_added(message)

    def _render(self, id_, ssml):
        path = 'tts.wav'
        with open(path, 'wb') as wave_file:
            self._swift.tts(wave_file, ssml)
        with open(path, 'rb') as wave_file:
            audio = wave_file.read()
        audio = audio.encode('base64')
        msg = ddp.MethodMessage(self._get_next_id(), 'setAudio', [id_, audio])
        self._conn.send(msg)

    def _send(self, message):
        self._conn.send(message)

    def connect(self):
        self._conn.connect()
        self._send(ddp.SubMessage(self._get_next_id(), 'ttsQueue'))

    def disconnect(self):
        self._conn.disconnect()


class TtsRequest(object):
    def __init__(self, id_, word, pitch=None, pitch_range=None, volume=None):
        self.id_ = id_
        self.word = word
        self.pitch = pitch
        self.pitch_range = pitch_range
        self.volume = volume


def main(argv=None):
    args = parse_args(argv=argv)
    configure_logging(args)

    url = ddp.ServerUrl(args.server)
    client = DdpClient(url)
    try:
        client.connect()
        handle_tts_requests(client)
    finally:
        try:
            client.disconnect()
        except:
            msg = 'An error occured while disconnecting from the DDP server'
            logger.exception(msg)
    return 0


def parse_args(argv=None):
    if argv is None:
        argv = sys.argv
    parser = ArgumentParser()
    parser.add_argument('-l', '--log-level', choices=LOG_NAME_TO_LEVEL.keys(),
                        default=LOG_LEVEL_TO_NAMES[logging.INFO])
    parser.add_argument('-s', '--server', default='127.0.0.1:3000')
    return parser.parse_args(args=argv[1:])


def configure_logging(args):
    global logger
    logging.basicConfig(datefmt='%H:%M:%S',
                        format='[%(levelname).1s %(asctime)s] %(message)s',
                        level=LOG_NAME_TO_LEVEL[args.log_level])
    logger = logging.getLogger(__name__)


def handle_tts_requests(client):
    raw_input()

if __name__ == '__main__':
    try:
        return_code = main()
    except KeyboardInterrupt:
        return_code = 1
    exit(return_code)

