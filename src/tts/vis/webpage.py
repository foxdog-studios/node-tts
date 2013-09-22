import logging
import os

from jinja2 import Environment, PackageLoader

from tts.utils import chunks


logger = logging.getLogger(__name__)

env = Environment(loader=PackageLoader('tts.vis', 'templates'))


COUNTER_PAGE_TEMPLATE = env.get_template('counter.jinja')
CREATING_PAGE_TEMPLATE = env.get_template('creation.jinja')
WEB_PAGE_TEMPLATE = env.get_template('popcorn.jinja')

WORDS_ITEM_HTML_TEMPLATE = """
<span id="w%(id)d" class="word"></span>
"""

PHRASE_ITEM_JS_TEMPLATE = """
"p%(id)d": {
    start: %(start)f,
    end: %(end)f,
    words: {
        %(words)s
    }
}
"""

WORD_ITEM_JS_TEMPLATE = """
"w%(id)d": {
    start: %(start)f,
    end: %(end)f,
    word: "%(word)s"
}
"""


class WebpageWriter:
    def __init__(self, build_dir, words_per_phrase=3):
        self._build_dir = build_dir
        self._words_per_phrase=words_per_phrase

    def write_counter_page(self, number_of_texts, number_of_notes):
        percent = number_of_texts / number_of_notes * 100
        if percent >= 100:
            percent = 100
            template = CREATING_PAGE_TEMPLATE
        else:
            template = COUNTER_PAGE_TEMPLATE

        if percent >= 100:
            audio_source = 'fat.ogg'
            image_source = 'meltingdino.gif'
        elif percent >= 66:
            audio_source = 'teenager.ogg'
            image_source = 'fatterdino.gif'
        elif percent >= 33:
            audio_source = 'kid.ogg'
            image_source = 'fatdino.gif'
        else:
            if percent > 0:
                audio_source = 'baby.ogg'
            else:
                audio_source = ''
            image_source = 'dino.gif'
        counter_page_data = {
            'audio_src': audio_source,
            'image_src': image_source,
            'width': percent,
            'number_of_texts': number_of_texts,
            'number_of_notes': number_of_notes,
        }
        text = template.render(**counter_page_data)
        self._write_index_html(text)

    def write_tts_page(self, mix_path, words, word_delays):
        logger.info('writing tts page %s\n%s\n%s', mix_path, words,
            word_delays)
        tts_data = {
            'audio_src': 'final_form.ogg',
            'popcorn_src': os.path.basename(mix_path),
            'words': self._build_words_html(),
            'phrases': self._build_phrases(words, word_delays),
        }
        self._write_index_html(WEB_PAGE_TEMPLATE.render(**tts_data))

    def _write_index_html(self, page_text):
        path = os.path.join(self._build_dir, 'index.html')
        with open(path, 'w') as web_page:
            web_page.write(page_text)

    def _build_phrases(self, words, word_delays):
        grouped_words = chunks(words, self._words_per_phrase)
        grouped_word_delays = list(chunks(word_delays, self._words_per_phrase))
        global_word_index = 0
        phrase_items_js = []
        for group_index, words_group in enumerate(grouped_words):
            if group_index >= len(grouped_word_delays):
                continue
            word_delays_group = grouped_word_delays[group_index]
            word_items_js = []
            min_start_time = float('inf')
            max_end_time = -float('inf')
            for word_index, word in enumerate(words_group):
                if word_index >= len(word_delays_group):
                    continue
                delay = word_delays_group[word_index]
                #XXX: Make the first word come in slightly early, to seem like
                # they synced
                if global_word_index < len(word_delays) -1:
                    word_end = word_delays[global_word_index + 1]
                else:
                    word_end = delay + 1
                if delay < min_start_time:
                    min_start_time = delay
                if word_end > max_end_time:
                    max_end_time = delay

                word_item_data = {
                    'id': word_index,
                    'start': delay,
                    'end': word_end,
                    'word': word,
                }

                word_items_js.append(WORD_ITEM_JS_TEMPLATE % word_item_data)
                global_word_index += 1
            if global_word_index < len(word_delays):
                max_end_time = word_delays[global_word_index]
            else:
                max_end_time = max_end_time + 10
            word_group_data = {
                'id': group_index,
                'start': min_start_time,
                'end': max_end_time,
                'words': ',\n'.join(word_items_js)
            }
            phrase_items_js.append(PHRASE_ITEM_JS_TEMPLATE % word_group_data)
        return ',\n'.join(phrase_items_js)

    def _build_words_html(self):
        html = []
        for index in range(self._words_per_phrase):
            word_data = {"id": index}
            html.append(WORDS_ITEM_HTML_TEMPLATE % word_data)
        return ''.join(html)

