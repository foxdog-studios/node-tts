# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import namedtuple
import re

from tts.rapping import constants
from tts.utils import count

note_matcher = re.compile(
    '\A([abcdefg]b?[012345678]|r)(?:_(\d+)(?:/(\d+))?)?\Z',
    re.IGNORECASE).match

Note = namedtuple('Note', ['pitch', 'start'])

class Melody(object):
    @classmethod
    def parse_melody(cls, bpm, raw_notes):
        spb = 60 / bpm
        start = 0
        notes = []

        for note in raw_notes.split():
            # Parse note
            match = note_matcher(note)
            if not match:
                raise ValueError('invalid note %r' % (note,))

            # Duration
            def get_int(group):
                i = match.group(group)
                return int(i) if i else 1
            n = get_int(2)
            d = get_int(3)
            beats = n / d
            duration = beats * spb

            # Note
            pitch = match.group(1)
            if pitch != 'r':
                pitch = getattr(constants, pitch[0].upper() + pitch[1:])
                note = Note(pitch, start)
                notes.append(note)

            start += duration

        return notes

