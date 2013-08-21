class MessageHandler:
    def __init__(self, message_cleaner, replies):
        assert replies, "must have at least one reply"
        self._replies = replies
        self._next_reply_index = 0
        self._message_cleaner = message_cleaner

    def _clean(self, message):
        return self._message_cleaner.clean(message)

    def _get_reply_body(self):
        i = self._next_reply_index
        body = self._replies[i]
        self._next_reply_index = (i + 1) % len(self._replies)
        return body

    def _build_reply(self, message):
        if message.number is not None:
            body = self._get_reply_body()
            return {'number': message.number, 'message': body}

    def handle(self, message):
        cleaned_message = self._clean(message)
        return self._build_reply(message)

