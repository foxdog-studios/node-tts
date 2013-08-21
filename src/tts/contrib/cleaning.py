from tts.messages.cleaning import (
    CleanerTemplate,
    clean,
    clean_char,
    keep,
    keep_char,
)


# =============================================================================
# = Cleaners                                                                  =
# =============================================================================

@clean
def clean_uppercase(word):
    return word.lower()


# =============================================================================
# = Keepers                                                                   =
# =============================================================================

keep_non_empty = keep(bool)
keep_alpha = keep_char(str.isalpha)

@keep
def keep_short(word):
    return len(word) < 15


@keep_char
def keep_ascii(char):
    return ord(char) < 2**7


# =============================================================================
# = Complex                                                                   =
# =============================================================================

class DictionaryCleaner(CleanerTemplate):
    def __init__(self, real_words):
        super().__init__()
        self._real_words = real_words

    def keep(self, word):
        return word in self._real_words

