import logging
import os

logger = logging.getLogger(__name__)

COUNTER_PAGE_TEMPLATE = """
<html>
<head>
    <script src="http://localhost:35729/livereload.js"></script>
    <style type="text/css">
        body {
            background-color: black;
            color: white;
        }
        .word {
           font-weight: bold;
           font-size: 185px;
           font-family: monospace;
           text-align: center;
           text-transform: uppercase;
           display: block;
        }
        .container {
            min-width: 100%%;
        }
        .power {
            font-size: 96px;
            display: inline-block;
            min-width: 33%%;
        }
        .power-image {
            margin-bottom: 50%%;
        }
        .number {
            display: inline-block;
            min-width: 66%%;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="power">
            <div>
                <img class="power-image" src="%(image_source)s" width="%(image_width)d%%"/>
            </div>
            <span>%(image_width)d%% </span><br/>
            <audio src="%(audio_source)s" autoplay/>
        </div>
        <div class="number">
            <div class="word">077</div>
            <div class="word">1719</div>
            <div class="word">1485</div>
        </div>
    </div>
</body>
</html>
"""

CREATING_PAGE_TEMPLATE = """
<html>
<head>
    <script src="http://localhost:35729/livereload.js"></script>
    <style type="text/css">
        body {
            background-color: black;
            color: white;
        }
        .word {
           font-weight: bold;
           font-size: 185px;
           font-family: monospace;
           text-align: center;
           text-transform: uppercase;
           display: block;
        }
        .container {
            min-width: 100%%;
        }
    </style>
</head>
<body>
    <div class="container">
        <div>
            <img class="power-image" src="%(image_source)s" height="%(image_width)d%%"/>
        </div>
    </div>
    <audio src="%(audio_source)s" autoplay loop/>
</body>
</html>
"""

WEB_PAGE_TEMPLATE = """
<html>
<head>
    <script src="jquery.js"></script>
    <script src="popcorn.js"></script>
    <script src="popcorn.applyclass.js"></script>
    <script src="popcorn.footnote.js"></script>
    <script src="http://localhost:35729/livereload.js"></script>
    <style type="text/css">
        body {
          background: url('finaldino.gif') no-repeat center center fixed black;
          background-size: 768px;
        }
        .word {
           color: grey;
           font-size: 190px;
           font-family: monospace;
           text-align: center;
           text-transform: uppercase;
           display: block;
          -webkit-text-stroke-width: 5px;
          -webkit-text-stroke-color: black;
        }
        .word.selected {
           color: white;
           font-weight: bold;
        }
        #overlay {
          display: none;
          position: absolute;
          left: 0%%; /* makes the div span all the way across the viewing area */
          top: 0%%; /* makes the div span all the way across the viewing area */
          background-color: black;
          -moz-opacity: 0.7; /* makes the div transparent, so you have a cool overlay effect */
          opacity: .70;
          filter: alpha(opacity=70);
          width: 100%%;
          height: 100%%;
          z-index: -90;
        }
    </style
    </style>
</head>
<body>
<div id="overlay">
</div>
<audio id="text-to-spit" src="%(audio_path)s"></audio>
<audio src="%(audio_source)s" autoplay></audio>
<div id="text">
    %(words)s
</div>
<script>
    var pop = Popcorn('#text-to-spit');
    var audio = document.getElementById('text-to-spit');
    var overlay = $('#overlay');
    var toggleControls = function() {
      overlay.toggle();
      pop.play();
    };
    document.onkeydown = function(evt) {
      evt = evt || window.event;
      if (evt.keyCode == 27) {
        toggleControls();
      }
    };

    var phrases = {%(phrases)s};

    $.each(phrases, function(pId, phrase) {
        $.each(phrase.words, function(wId, word) {
            pop.footnote({
                start: phrase.start,
                end: phrase.end,
                text: word.word,
                target: wId,
            });
            pop.footnote({
                start: word.start,
                end: word.end,
                text: '',
                target: wId,
                effect: 'applyclass',
                applyclass: 'selected'
            });
        });
    });
</script>
</body>
</html>
"""

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
        # Never go over 100%
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
            'audio_source': audio_source,
            'image_source': image_source,
            'image_width': percent,
            'number_of_texts': number_of_texts,
            'number_of_notes': number_of_notes,
        }
        self._write_index_html(template % counter_page_data)

    def write_tts_page(self, mix_path, words, word_delays):
        logger.info('writing tts page %s\n%s\n%s', mix_path, words,
            word_delays)
        tts_data = {
            'audio_source': 'final_form.ogg',
            'audio_path': os.path.basename(mix_path),
            'words': self._build_words_html(),
            'phrases': self._build_phrases(words, word_delays),
        }
        self._write_index_html(WEB_PAGE_TEMPLATE % tts_data)

    def _write_index_html(self, page_text):
        with open(os.path.join(self._build_dir, 'index.html'), 'w') as web_page:
            web_page.write(page_text)

    def _build_phrases(self, words, word_delays):
        def chunks(l, n):
            for i in range(0, len(l), n):
                    yield l[i:i+n]
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
                if global_word_index == 0 and delay > 0:
                    delay -= 0.1
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
            word_data = {
                "id": index,
            }
            html.append(WORDS_ITEM_HTML_TEMPLATE % word_data)
        return ''.join(html)

