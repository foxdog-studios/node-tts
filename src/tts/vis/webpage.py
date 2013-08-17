import logging
import os

logger = logging.getLogger(__name__)

WEB_PAGE_TEMPLATE = """
<html>
<head>
    <script src="jquery.js"></script>
    <script src="popcorn.js"></script>
    <script src="popcorn.applyclass.js"></script>
    <script src="popcorn.footnote.js"></script>
    <style type="text/css">
        .word {
           color: red;
        }
        .word:hover, .word.selected {
            color: blue;
            cursor: pointer;
        }
    </style>
</head>
<body>
<audio id="text-to-spit" src="%(audio_path)s" controls></audio>
<div id="text">
    %(words)s
</div>
<script>
    var pop = Popcorn('#text-to-spit');
    var wordDelays = {%(word_delays)s};

    $.each(wordDelays, function(id, time) {
      pop.footnote({
        start: time.start,
        end: time.end,
        text: '',
        target: id,
        effect: "applyclass",
        applyclass: "selected"
      });
    });

    pop.play();

    $('.word').click(function() {
        var audio = $('#text-to-spit');
        audio[0].currentTime = parseFloat($(this).data('start'), 10);
        audio[0].play();
    });

</script>
</body>
</html>
"""

WORD_DELAYS_ITEM_JS_TEMPLATE = """
    "w%(id)d": {start: %(start)f, end: %(end)f}
"""

WORDS_ITEM_HTML_TEMPLATE = """
<span id="w%(id)d" class="word" data-start="%(data_start)f">%(word)s</span>
"""


class WebpageWriter:
    def __init__(self, build_dir):
        self._build_dir = build_dir

    def write_tts_page(self, mix_path, words, word_delays):
        logger.info('writing tts page %s\n%s\n%s', mix_path, words,
            word_delays)
        tts_data = {
            'audio_path': os.path.basename(mix_path),
            'words': self._build_words_html(words, word_delays),
            'word_delays': self._build_word_delays_js(word_delays),
        }
        with open(os.path.join(self._build_dir, 'index.html'), 'w') as web_page:
            web_page.write(WEB_PAGE_TEMPLATE % tts_data)

    def _build_word_delays_js(self, word_delays):
        #XXX: Don't know their length, for now just add a second
        word_delays_js = []
        for index, word_delay in enumerate(word_delays):
            if index < len(word_delays) - 1:
                word_end = word_delays[index + 1]
            else:
                word_end = word_delay + 1
            word_delay_data = {
                "id": index,
                "start": word_delay,
                "end": word_end,
            }
            js = WORD_DELAYS_ITEM_JS_TEMPLATE % word_delay_data
            # Valid json, commas on all but the last item
            if index < len(word_delays) - 1:
                js = "%s," % (js)
            word_delays_js.append(js)
        return ''.join(word_delays_js)

    def _build_words_html(self, words, word_delays):
        html = []
        for index, word in enumerate(words):
            word_delay = word_delays[index]
            word_data = {
                "id": index,
                "data_start": word_delay,
                "word": word,
            }
            html.append(WORDS_ITEM_HTML_TEMPLATE % word_data)
        return ''.join(html)

