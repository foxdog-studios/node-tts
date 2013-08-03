import re

from tts import constants


note_matcher = re.compile(
    '\A([abcdefg]b?[012345678]|r)(?:_(\d+)(?:/(\d+))?)?\Z',
    re.IGNORECASE).match

def parse_melody(notes):
    ns = []
    for note in notes.split():
        match = note_matcher(note)
        if not match:
            raise ValueError('Invalid note %r.' % note)
        pitch = match.group(1)
        if pitch == 'r':
            pitch = constants.REST
        else:
            pitch = getattr(constants, pitch[0].upper() + pitch[1:])
        n = match.group(2)
        n = int(n) if n else 1
        d = match.group(3)
        d = int(d) if d else 1
        ns.append((pitch, n / d))
    return ns


