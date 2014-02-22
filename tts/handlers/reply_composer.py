from itertools import cycle

from tts.sms import SmsReply

class ReplyComposer:
    def __init__(self, replies):
        if not replies:
            raise ValueError('at least one reply must be given')
        self._replies = cycle(replies)

    def handle(self, sms):
        number = sms.number
        message = next(self._replies)
        return [SmsReply(number, message, sms)]

