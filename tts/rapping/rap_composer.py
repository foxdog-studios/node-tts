# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil
import subprocess
import tempfile

from tts.rapping.constants import X_LOW


class RapRenderer(object):
    def __init__(self, tts, melody, backing_track):
        self._backing_track = backing_track
        self._melody = melody
        self._sox_path = '/usr/bin/sox'
        self._tts = tts
        self._words = []

    def add_words(self, words):
        excess = len(words) + len(self._words) - len(self._melody)
        if excess > 0:
            words = words[:-excess]
        self._words.extend(words)

    def has_enough_words(self):
        return len(self._words) == len(self._melody)

    def render(self):
        assert self.has_enough_words()

        delays = []
        dir_path = tempfile.mkdtemp(prefix='tts-')
        iterable = enumerate(zip(self._words, self._melody))
        word_paths = []

        for i, (word, (pitch, start)) in iterable:
            delays.append(start)
            wave_path = os.path.join(dir_path, '%s.wav' % (i,))
            word_paths.append(wave_path)
            with open(wave_path, 'wb') as wave_file:
                self._tts.tts(wave_file, word, pitch=pitch, pitch_range=X_LOW)

        rap_path = os.path.join(dir_path, 'rap.wav')
        channels = ','.join(str(channel)
                            for channel in range(1, len(self._words) + 2))
        args = (
              [self._sox_path, '-M']
            + word_paths
            + [self._backing_track, rap_path, 'delay']
            + [str(delay) for delay in delays]
            + ['remix', channels, 'norm']
        )
        subprocess.check_call(args)

        return rap_path

