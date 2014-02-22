from tts.utils import format_obj

class SmsReply:
    def __init__(self, number, message, reply_to):
        self.number = number
        self.message = message
        self.reply_to = reply_to

    def __str__(self):
        return format_obj('[{number}] {message} (Reply to: {reply_to})', self)

