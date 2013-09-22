class Message:
    _next_id = 0

    def __init__(self, number, message):
        self.id = self._next_id
        self._next_id += 1
        self.number = number
        self.message = message

    def __str__(self):
        return '%d, %s: %s' % (self.id, self.number, self.message)

