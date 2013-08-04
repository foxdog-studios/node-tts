#!/usr/bin/env python

from argparse import ArgumentParser
from collections import OrderedDict
import logging
import pickle
import queue
import os
import shutil
import sys

from tts.melody import parse_melody
from tts.sms.worker import SmsHandler
from tts.sms.server import SmsServer
from tts.swift import Swift
from tts.syllables import Syllables

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


def build_argument_parser():
    parser = ArgumentParser()
    parser.add_argument('-b', '--bpm', default=120, type=float, help='rap BPM')
    parser.add_argument('-H', '--host', help='host to bind to')
    parser.add_argument('-l', '--log-level', choices=LOG_NAME_TO_LEVEL.keys(),
                        default=LOG_LEVEL_TO_NAMES[logging.INFO])
    parser.add_argument('-p', '--port', type=int, help='server port')
    parser.add_argument('-r', '--reply', help='The reply message.')
    parser.add_argument('-s', '--backing-sample', help='backing sample')
    parser.add_argument('-t', '--threshold', default=0.2, type=float,
                        help='volume at which a word sample starts')
    parser.add_argument('-w', '--words', help='acceptable words')
    parser.add_argument('phonemes', help='phonemes for syllable splitting')
    parser.add_argument('backing_track', help='backing track to rap over')
    parser.add_argument('melody', help='melody to rap to')
    return parser


def main(argv=None):
    global logger

    if argv is None:
        argv = sys.argv
    args = build_argument_parser().parse_args(args=argv[1:])

    logging.basicConfig(
            datefmt='%H:%M:%S',
            format='[%(levelname).1s %(asctime)s] %(message)s',
            level=LOG_NAME_TO_LEVEL[args.log_level])
    logger = logging.getLogger(__name__)

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

    sms_handler = SmsHandler(
        syllables,
        incoming_sms,
        swift,
        args.backing_track,
        melody,
        bpm=args.bpm,
    )
    sms_handler.start();

    server = SmsServer(
        incoming_sms,
        host=args.host,
        port=args.port,
        reply=args.reply,
    )
    server.mainloop();

    sms_handler.join()

    logger.info('Finished')

    return 0


if __name__ == '__main__':
    try:
        return_code = main()
    except KeyboardInterrupt:
        return_code = 1
    exit(return_code)

