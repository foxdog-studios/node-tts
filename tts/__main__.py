# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from argparse import ArgumentParser
from collections import OrderedDict
import logging
import os
import sys

import cherrypy

from tts.conf import Configuration
from tts.dino_client import DinoClient
from tts.handlers import (
    Cleaner,
    DinoForwarder,
    NullHandler,
    PipelineHandler,
    Rapper,
    ReplyComposer,
)
from tts.server import Server
from tts.rapping.melody import Melody
from tts.rapping.rap_composer import RapComposer
from tts.rapping.text_to_speech import TextToSpeech


def build_argument_parser():
    parser = ArgumentParser()
    parser.add_argument('-c', '--conf', help='path to YAML configuration file')
    return parser


def main(argv=None):
    global logger

    if argv is None:
        argv = sys.argv
    args = build_argument_parser().parse_args(args=argv[1:])

    conf = Configuration(path=args.conf)

    # If configuration was loaded from a file, reload if that file
    # changes
    if conf.path is not None:
        cherrypy.engine.autoreload.files.add(conf.path)

    melody = Melody.parse_melody(conf.bpm, conf.melody)

    # Build the handler pipeline
    handlers = []
    if conf.handlers_cleaner:
        handlers.append(Cleaner.from_path(conf.handlers_cleaner))

    vis_client = None
    if conf.handlers_vis_host:
        dino_client = DinoClient(conf.handlers_vis_host)
        dino_client.connect()
        dino_client.reset(len(melody))
        dino_forwarder = DinoForwarder(dino_client)
        handlers.append(dino_forwarder)

    if conf.handlers_rapper:
        tts = TextToSpeech()
        backing_track = conf.handlers_rapper
        rap_composer = RapComposer(tts, melody, backing_track)
        handlers.append(Rapper(rap_composer))

    if conf.handlers_reply_composer:
        handlers.append(ReplyComposer(conf.replies))

    if not handlers:
        handlers.append(NullHandler())

    root = Server(PipelineHandler(handlers))

    # Configure and stary the CherryPy engine
    cherrypy.config.update({
        'server.socket_host': conf.server_host,
        'server.socket_port': conf.server_port,
    })
    cherrypy.quickstart(root=root, script_name='', config={'/': {}})

    if dino_client is not None:
        dino_client.disconnect()

    return 0


if __name__ == '__main__':
    try:
        return_code = main()
    except KeyboardInterrupt:
        return_code = 1
    exit(return_code)

