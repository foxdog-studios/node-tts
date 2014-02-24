# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from argparse import ArgumentParser
import sys

import cherrypy

from tts import server
from tts.config import Configuration
from tts.dino_client import DinoClient
from tts.rapping.melody import Melody
from tts.rap_composer import RapComposer
from tts.reply_composer import ReplyComposer
from tts.handlers.cleaner import Cleaner
from tts.rapping.text_to_speech import TextToSpeech
from tts.rapping.rap_composer import RapRenderer


def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = build_argument_parser().parse_args(args=argv[1:])
    config = Configuration(path=args.config)
    melody = Melody.parse_melody(config.bpm, config.melody)
    dino_client = DinoClient('127.0.0.1:3000')
    dino_client.connect()
    dino_client.reset(len(melody))
    cleaner = Cleaner.from_path(config.dictionary)
    tts = TextToSpeech()
    rap_renderer = RapRenderer(tts, melody, config.backing_track)
    reply_composer = ReplyComposer(config.replies)
    with RapComposer(dino_client, cleaner, rap_renderer) as rap_composer:
        server.start(config, rap_composer, reply_composer)
    dino_client.disconnect()


def build_argument_parser():
    parser = ArgumentParser()
    parser.add_argument('config', help='path to YAML configuration file')
    return parser


if __name__ == '__main__':
    try:
        return_code = main()
    except KeyboardInterrupt:
        return_code = 1
    exit(return_code)

