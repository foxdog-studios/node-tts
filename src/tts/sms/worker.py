import functools
import multiprocessing
import os
import queue
import subprocess
import time

import cherrypy

from tts.constants import REST
from tts.dictionary import Dictionary


class SmsHandler:

    dictionary_path = None
    play_path = None
    sox_path = None

    def __init__(self, syllables, sms_queue, swift, backing_sample, melody,
                 output_dir, webpage_writer, bpm=100, dummy=False):
        super().__init__()
        self.daemon = True
        self._syllables = syllables
        self._sms_queue = sms_queue
        self._melody = melody
        self._output_dir = output_dir
        self._spb = 60 / bpm
        self._speech = []
        self._rap_mode = False
        self._rap_path = None
        self._swift = swift
        self._webpage_writer = webpage_writer
        self._backing_sample = backing_sample
        self._dummy = dummy

    def run(self):
        self._real_words = set()
        if self.dictionary_path is not None:
            self._real_words = Dictionary.from_path(self.dictionary_path)

        num_syllables = self._get_number_of_syllables()
        num_notes = self._get_number_of_notes()
        self._update_counter_page(num_syllables, num_notes)
        while not self._stop_event.is_set():
            try:
                msg = self._sms_queue.get_nowait()
            except queue.Empty:
                time.sleep(0.1)
                continue
            msg_id = msg.id
            number = msg.number
            message = msg.message
            self.render_speech(message)
            num_syllables = self._get_number_of_syllables()
            num_notes = self._get_number_of_notes()
            self._update_counter_page(num_syllables, num_notes)
            if num_syllables >= num_notes:
                self._compile_rap(msg_id)
            self._sms_queue.task_done()

    def _compile_rap(self, msg_id):
        cherrypy.log('Entering rap mode, compiling rap')
        self._rap_mode = True
        self._rap_path = self.render_rap(msg_id, self._speech)
        cherrypy.log('Rap compilied')

    def _update_counter_page(self, num_syllables, num_notes):
        cherrypy.log('%d/%d syllables sent so far'
                     % (num_syllables, num_notes))
        self._webpage_writer.write_counter_page(num_syllables, num_notes)

    def _get_number_of_notes(self):
        return sum(1 for pitch, beats in self._melody if pitch != REST)

    def _get_number_of_syllables(self):
        lexicon, translate = self._syllables.build_lexicon(set(self._speech))
        num_syllables = 0
        for word in self._speech:
            if word in translate:
                num_syllables += len(translate[word])
            else:
                num_syllables += 1
        return num_syllables

    def render_speech(self, message):
        words = self.clean_message(message)
        if words:
            self._speech.extend(words)

    def render_rap(self, msg_id, words):

        lexicon, translate = self._syllables.build_lexicon(set(words))

        lexpath = '/tmp/%d-lexicon.txt' % (msg_id,)
        with open(lexpath, 'w') as out:
            for word, phonemes in lexicon.items():
                out.write('%s 0 %s\n' % (word, ' '.join(phonemes)))

        trans_words = []
        original_words = list(words)
        word_gaps = []
        for word in words:
            if word in translate:
                transalation = translate[word]
                word_gaps.append(len(transalation))
                trans_words.extend(transalation)
            else:
                word_gaps.append(1)
                trans_words.append(word)
        words = trans_words

        cherrypy.log(str(words))
        cherrypy.log(str(word_gaps))

        # Make the length of words fit the melody
        notes = self._get_number_of_notes()
        diff = notes - len(words)
        if diff < 0:
            words = words[:diff]
        else:
            words = words + ['la'] * diff

        delay = 0
        gap_index = 0
        current_gap = 0
        current_gap_limit = word_gaps[gap_index]
        original_word_delays = []
        offsets = {}
        word_index = 0
        word_count = len(words)
        word_delays = []
        word_paths = []

        pool = multiprocessing.Pool()

        for pitch, beats in self._melody:
            duration = beats * self._spb

            if pitch != REST:
                word = words[word_index]
                word_delays.append(delay)
                word_path = '/tmp/%s-%s.wav' % (msg_id, word_index)
                word_paths.append(word_path)
                ssml = '<s><prosody pitch="%sHz" range="x-low">%s</prosody></s>' \
                    % (pitch, word)
                func = functools.partial(offsets.__setitem__, word_index)
                pool.apply_async(text_to_speech,
                                 (self._swift, ssml, word_path, lexpath),
                                 callback=func)
                current_gap += 1
                if current_gap == 0 and gap_index == 0:
                    original_word_delays.append((word_index, delay))
                elif current_gap >= current_gap_limit \
                        and gap_index < len(word_gaps):
                    current_gap = 0
                    gap_index += 1
                    original_word_delays.append((word_index, delay))
                    if gap_index < len(word_gaps):
                        current_gap_limit = word_gaps[gap_index]
                word_index += 1

            delay += duration

            if word_index == word_count:
                # Break here, rather than inside the if statement above, so that
                # that delay is updated and equals the duration of the rap.
                break

        pool.close()
        pool.join()

        if not word_index:
            # Didn't render any words!
            return

        # Apply the offsets
        word_delays = [delay + offsets[i] for i, delay in enumerate(word_delays)]
        word_delays = [d if d >= 0 else 0 for d in word_delays]

        offset_original_word_delays = []
        for index, delay in original_word_delays:
            offset = offsets[index]
            offset_original_word_delays.append(delay + offset)
        offset_original_word_delays = [d if d >= 0 else 0 \
                for d in offset_original_word_delays]

        # Mix the rap and the backing track
        mix_path = os.path.join(self._output_dir, '%s-mix.wav' % (msg_id,))
        sox_args = [self.sox_path, '-M'] + word_paths \
            + [self._backing_sample, mix_path, 'delay'] \
            + list(map(str, word_delays)) \
            + ['remix',
                ','.join(str(channel) for channel in range(1, word_count + 2)),
                'norm']
        cherrypy.log(' '.join(sox_args))
        if not self._dummy:
            subprocess.check_call(sox_args)

        self._webpage_writer.write_tts_page(mix_path,
                                            original_words,
                                            offset_original_word_delays)

        return mix_path

    def clean_message(self, message):
        words = []
        for word in message.split():
            chars = [c for c in word if c.isalpha()]
            if chars:
                word = ''.join(chars).lower()
                if not self._real_words or word in self._real_words:
                    words.append(word)
        return words


def text_to_speech(swift, ssml, word_path, lexicon):
    return swift.tts_file(ssml, word_path, lexicon=lexicon)

