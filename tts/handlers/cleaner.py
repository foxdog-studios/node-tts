from tts.sms import Sms

class Cleaner:
    def __init__(self, words):
        self._words = words

    def handle(self, sms):
        msg = sms.message
        msg = msg.lower()
        words = []
        for word in msg.split():
            word = ''.join(c for c in word if c.isalpha())
            if word in self._words:
                words.append(word)
        msg = ' '.join(words)
        return Sms(sms.number, msg, original=sms)

    @classmethod
    def from_path(cls, path):
        words = set()
        with open(path) as words_file:
            for line in words_file:
                line = line.strip()
                if line.isalpha():
                    words.add(line.lower())
        return cls(words)

