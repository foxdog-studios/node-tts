# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import yaml


class Configuration(object):
    def __init__(self, path):
        with open(path) as conf_file:
            self._config = yaml.load(conf_file)
        self._path = path

    @property
    def bpm(self):
        return self._config['bpm']

    @property
    def dictionary(self):
        return self._config['dictionary']

    @property
    def dino_address(self):
        return self._config['dino']['address']

    @property
    def backing_track(self):
        return self._config['backing_track']

    @property
    def melody(self):
        with open(self._config['melody']) as melody_file:
            return melody_file.read()

    @property
    def path(self):
        return self._path

    @property
    def replies(self):
        return list(self._config['replies'])

    @property
    def tts_host(self):
        return self._config['tts']['host']

    @property
    def tts_port(self):
        return self._config['tts']['port']
