# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import multiprocessing
import os
import shutil
import subprocess
import tempfile

from tts.rapping.constants import X_LOW
from tts.rapping.text_to_speech import TextToSpeech


class RapRenderer(object):
    def __init__(self, melody, backing_track):
        self._backing_track = backing_track
        self._melody = melody
        self._sox_path = '/usr/bin/sox'
        self._words = []

    def add_words(self, words):
        excess = len(words) + len(self._words) - len(self._melody)
        if excess > 0:
            words = words[:-excess]
        self._words.extend(words)

    def get_timed_words(self):
        return zip(self._words, self._melody)

    def has_enough_words(self):
        return len(self._words) == len(self._melody)

    def render(self):
        assert self.has_enough_words()

        delays = []
        dir_path = tempfile.mkdtemp(prefix='tts-')
        iterable = enumerate(self.get_timed_words())
        word_paths = []

        pool = multiprocessing.Pool(multiprocessing.cpu_count() * 3)

        for i, (word, (pitch, start)) in iterable:
            delays.append(start)
            wave_path = os.path.join(dir_path, '%s.wav' % (i,))
            word_paths.append(wave_path)
            pool.apply_async(_tts, (wave_path, word, pitch))

        pool.close()
        pool.join()

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


def _tts(wave_path, word, pitch):
    tts = TextToSpeech()
    print
    with open(wave_path, 'wb') as wave_file:
        tts.tts(wave_file, word, pitch=pitch, pitch_range=X_LOW)

