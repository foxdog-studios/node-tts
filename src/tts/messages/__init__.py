class Message:
    def __init__(self, body, number=None):
        self.number = number
        self.body = body

    def __str__(self):
        parts = []
        if self.number is not None:
            parts.append(self.number)
        parts.append(self.body)
        return ': '.join(parts)

