import os
import tempfile
import unittest

from tts.handlers import Cleaner
from tts.sms import Sms
from tts.rapping import constants
from tts.rapping.melody import parse_melody
from tts.rapping.rap_composer import RapComposer
from tts.rapping.text_to_speech import TextToSpeech


class CleanerTestCase(unittest.TestCase):
    def setUp(self):
        self.cleaner = Cleaner.from_path('/usr/share/dict/cracklib-small')

    def _test(self, message, expected):
        result = self.cleaner.handle(Sms('+44700900000', message))
        self.assertEqual(result.message, expected)

    def test_ascii(self):
        self._test('te2st%  []2message  ', 'test message')

    def test_lowercase(self):
        self._test('TeSt MesSaGe', 'test message')

    def test_squeeze_spaces(self):
        self._test('test   message', 'test message')


class RapComposerTestCase(unittest.TestCase):

    MELODY = '''
        r_7
                                                        B3_1/2  A3_1/2
        B3_1/2  Gb3_1/2 D3_1/2  Gb3_1/2 B2              B3_1/2  A3_1/2
        B3_1/2  Gb3_1/2 D3_1/2  Gb3_1/2 B2              B3_1/2  Db4_1/2
        D4_1/2  Db4_1/2 D4_1/2  B3_1/2  Db4_1/2 B3_1/2  Db4_1/2 A3_1/2
        B3_1/2  A3_1/2  B3_1/2  G3_1/2  B2              B3_1/2  A3_1/2
        B3_1/2  Gb3_1/2 D3_1/2  Gb3_1/2 B2              B3_1/2  A3_1/2
        B3_1/2  Gb3_1/2 D3_1/2  Gb3_1/2 B2              B3_1/2  Db4_1/2
        D4_1/2  Db4_1/2 D4_1/2  B3_1/2  Db4_1/2 B3_1/2  Db4_1/2 A3_1/2
        B3_1/2  A3_1/2  B3_1/2  Db4_1/2 D4              Gb4_1/2 E4_1/2
        Gb4_1/2 D4_1/2  A3_1/2  D4_1/2  Gb3             Gb4_1/2 E4_1/2
        Gb4_1/2 D4_1/2  A3_1/2  D4_1/2  Gb3             Gb4_1/2 Ab4_1/2
        A4_1/2  Ab4_1/2 A4_1/2  Gb4_1/2 Ab4_1/2 Gb4_1/2 Ab4_1/2 E4_1/2
        Ab4_1/2 E4_1/2  Db4_1/2 E4_1/2  Ab4             Gb4_1/2 E4_1/2
        Gb4_1/2 D4_1/2  A3_1/2  D4_1/2  Gb3             Gb4_1/2 E4_1/2
        Gb4_1/2 D4_1/2  A3_1/2  D4_1/2  Gb3             Gb4_1/2 Ab4_1/2
        A4_1/2  Ab4_1/2 A4_1/2  Gb4_1/2 Ab4_1/2 Gb4_1/2 Ab4_1/2 E4_1/2
        Ab4_1/2 E4_1/2  Db4_1/2 E4_1/2  Ab4
    '''

    def setUp(self):
        tts = TextToSpeech()
        self._melody = parse_melody(90, self.MELODY)
        backing_track = os.path.join(os.path.dirname(__file__),
                                     'backing_tracks/default.wav')
        self._composer = RapComposer(tts, self._melody, backing_track)

    def test_compose(self):
        words = ['la'] * len(self._melody)
        self._composer.add_words(words)
        self._composer.render()


class TextToSpeechTestCase(unittest.TestCase):
    def setUp(self):
        self._text_to_speech = TextToSpeech()

    def tts(self, *args, **kwargs):
        return self._text_to_speech.tts(*args, **kwargs)

    def test_tts(self):
        # This only tests that is doesn't throw an exception, not that
        # it does it correctly.
        with tempfile.TemporaryFile() as wave_file:
            self.tts(wave_file, 'Hello world', pitch=constants.A4,
                     pitch_range=constants.X_LOW)


if __name__ == '__main__':
    unittest.main()

