from tts.util import default, identity

class CleanedMessage:
    def __init__(self, words, number=None, original=None):
        self.number = number
        self.original = original
        self.words = words

    def __str__(self):
        parts = []
        if self.number is not None:
            parts.append(self.number)
        parts.append(' '.join(self.words))
        return ': '.join(parts)


class MessageCleaner:
    def __init__(self, cleaners, word_splitter=None):
        self._cleaners = list(cleaners)
        self._word_splitter = default(word_splitter, WhiteSpaceWordSplitter())

    def _apply_cleaners(self, words):
        for cleaner in self._cleaners:
            words = cleaner(words)
        return words

    def _build_cleaned_message(self, words, original):
        return CleanedMessage(words, number=original.number, original=original)

    def _clean_body(self, body):
        words = self._split_words(body)
        return self._apply_cleaners(words)

    def _split_words(self, body):
        return self._word_splitter(body)

    def clean(self, message):
        words = self._clean_body(message.body)
        return self._build_cleaned_message(words, message)


class WhiteSpaceWordSplitter:
    def __call__(self, body):
        return body.split()


class Cleaner:
    def __init__(self, clean=None, keep=None, reconstruct=None):
        self._clean = default(clean, identity)
        self._keep = default(keep, lambda w: True)
        self._reconstruct = default(reconstruct, list)

    def __call__(self, iterable):
        return self._reconstruct(self._clean(item)
                                 for item in iterable if self._keep(item))


class CharCleaner():
    def __init__(self, clean=None, keep=None, reconstruct=None):
        reconstruct = default(reconstruct, self._reconstruct_word)
        self._char_cleaner = Cleaner(clean=clean, keep=keep,
                                     reconstruct=reconstruct)
        self._word_cleaner = Cleaner(clean=self._char_cleaner)

    def __call__(self, words):
        return self._word_cleaner(words)

    def _reconstruct_word(self, chars):
        return ''.join(chars)


class CleanerTemplate:
    cleaner_cls = Cleaner

    def __init__(self):
        def get(name):
            return getattr(self, name, None)
        self._cleaner = self.cleaner_cls(clean=get('clean'), keep=get('keep'),
                                         reconstruct=get('reconstruct'))

    def __call__(self, iterable):
        return self._cleaner(iterable)


class CharCleanerTemplate(CleanerTemplate):
    cleaner_cls = CharCleaner


def clean(func):
    return Cleaner(clean=func)


def keep(func):
    return Cleaner(keep=func)


def clean_char(func):
    return CharCleaner(clean=func)


def keep_char(func):
    return CharCleaner(keep=func)

