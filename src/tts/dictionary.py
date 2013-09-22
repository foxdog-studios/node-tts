class Dictionary:
    def __init__(self, words):
        self._words = frozenset(words)

    def __bool__(self):
        return bool(self._words)

    def __contains__(self, word):
        return word in self._words

    @classmethod
    def from_path(cls, path):
        words = set()
        with open(path) as file:
            for line in file:
                line = line.strip().lower()
                if line.isalpha():
                    words.add(line)
        return cls(words)

