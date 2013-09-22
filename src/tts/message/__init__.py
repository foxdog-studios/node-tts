class Message:
    def __init__(self, number, message):
        self.number = number
        self.message = message

    def __str__(self):
        return '%s: %s' % (self.number, self.message)

