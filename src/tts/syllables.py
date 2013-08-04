PHONEMES_CMU_TO_CEPSTRAL = {
    'AA': 'aa',
    'AE': 'ae',
    'AH': 'ah',
    'AO': 'ao',
    'AW': 'aw',
    'AY': 'ay',
    'B' : 'b' ,
    'CH': 'ch',
    'D' : 'd' ,
    'DH': 'dh',
    'EH': 'eh',
    'ER': 'er',
    'EY': 'ey',
    'F' : 'f' ,
    'G' : 'g' ,
    'HH': 'h' ,
    'IH': 'ih',
    'IY': 'i' ,
    'JH': 'jh',
    'K' : 'k' ,
    'L' : 'l' ,
    'M' : 'm' ,
    'N' : 'n' ,
    'NG': 'ng',
    'OW': 'ow',
    'OY': 'oy',
    'P' : 'p' ,
    'R' : 'r' ,
    'S' : 's' ,
    'SH': 'sh',
    'T' : 't' ,
    'TH': 'th',
    'UH': 'uh',
    'UW': 'uw',
    'V' : 'v' ,
    'W' : 'w' ,
    'Y' : 'j' ,
    'Z' : 'z' ,
    'ZH': 'zh',
}

STRESSES_CMU_TO_CEPSTRAL = {
    '0': '0',
    '1': '1',
    '2': '0',
}


class Syllables:
    def __init__(self, phonemes):
        self._phonemes = phonemes

    def cmu_to_cepstral(self, cmu):
        cepstral = []
        for phoneme in cmu:
            if self.is_vowel(phoneme):
                stress = STRESSES_CMU_TO_CEPSTRAL[phoneme[-1]]
                phoneme = phoneme[:-1]
            else:
                stress = ''
            cepstral.append(PHONEMES_CMU_TO_CEPSTRAL[phoneme] + stress)
        return cepstral

    def is_vowel(self, phoneme):
        return phoneme[-1].isdigit()

    def split_syllable(self, phonemes):
        syllables = []
        syllable = []
        for phoneme in phonemes:
            syllable.append(phoneme)
            if self.is_vowel(phoneme):
                syllables.append(syllable)
                syllable = []
        if syllable:
            if syllables:
                syllables[-1].extend(syllable)
            else:
                syllables.append(syllable)
        return syllables

    def build_lexicon(self, words):
        lexicon = {}
        translate = {}
        for word in words:
            if word not in self._phonemes:
                continue
            trans_words = []
            phonemes = min(self._phonemes[word], key=len)
            phonemes = self.cmu_to_cepstral(phonemes)
            for syllable in self.split_syllable(phonemes):
                trans_word = hex(len(lexicon))[2:]
                trans_words.append(trans_word)
                lexicon[trans_word] = syllable
            translate[word] = trans_words
        return lexicon, translate

