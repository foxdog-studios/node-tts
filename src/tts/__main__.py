from argparse import ArgumentParser
from collections import OrderedDict
import pickle
import queue
import os
import shutil
import sys
import threading

from cherrypy.process import plugins
import cherrypy

from tts.config import Configuration
from tts.melody import parse_melody
from tts.sms.worker import SmsHandler
from tts.sms.server import SmsServer
from tts.swift import Swift
from tts.syllables import Syllables
from tts.vis.webpage import WebpageWriter


class SmsHandlerPlugin(plugins.SimplePlugin):
    def __init__(self, engine, sms_handler):
        super().__init__(engine)
        self._sms_handler = sms_handler
        self._sms_handler._stop_event = threading.Event()

    def start(self):
        self._thread = threading.Thread(target=self._sms_handler.run,
                                        name='SMS handler')
        self._thread.start()

    def stop(self):
        self._sms_handler._stop_event.set()
        self._thread.join()


def build_argument_parser():
    parser = ArgumentParser()
    parser.add_argument('-b', '--bpm', default=120, type=float, help='rap BPM')
    parser.add_argument('-c', '--config')
    parser.add_argument('-d', '--dummy', action='store_true', default=False,
                        help='do not render any audio')
    parser.add_argument('-H', '--host', help='host to bind to')
    parser.add_argument('-o', '--output-dir', help='directory to place output')
    parser.add_argument('-p', '--port', type=int, help='server port')
    parser.add_argument('-r', '--reply', help='reply message')
    parser.add_argument('-s', '--backing-sample', help='backing sample')
    parser.add_argument('-t', '--threshold', default=0.2, type=float,
                        help='volume at which a word sample starts')
    parser.add_argument('-w', '--words', help='acceptable words')
    parser.add_argument('phonemes', help='phonemes for syllable splitting')
    parser.add_argument('backing_track', help='backing track to rap over')
    parser.add_argument('melody', help='melody to rap to')
    return parser


def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = build_argument_parser().parse_args(args=argv[1:])

    config = Configuration(args.config)

    SmsHandler.dictionary_path = args.words
    SmsHandler.play_path = shutil.which('play')
    SmsHandler.sox_path = shutil.which('sox')

    incoming_sms = queue.Queue()
    swift = Swift(shutil.which('swift'))

    with open(args.melody) as melody_file:
        melody = melody_file.read()
    melody = parse_melody(melody)

    with open(args.phonemes, 'rb') as infile:
        phonemes = pickle.load(infile)
    syllables = Syllables(phonemes)

    sms_handler = SmsHandlerPlugin(cherrypy.engine, SmsHandler(
        syllables,
        incoming_sms,
        swift,
        args.backing_track,
        melody,
        args.output_dir + '/audio',
        WebpageWriter(args.output_dir),
        bpm=args.bpm,
        dummy=args.dummy
    ))
    sms_handler.subscribe()

    server = SmsServer(
        incoming_sms,
        host=args.host,
        port=args.port,
        replies=config.replies,
    )
    server.serve();

    return 0


if __name__ == '__main__':
    try:
        return_code = main()
    except KeyboardInterrupt:
        return_code = 1
    exit(return_code)

