class Rapper:
    def __init__(self, rap_composer):
        self._rap_composer = rap_composer

    def handle(self, sms):
        words = sms.message.split()
        self._rap_composer.add_words(words)
        return sms

