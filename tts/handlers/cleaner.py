# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


class Cleaner(object):
    def __init__(self, words):
        self._words = words

    def clean(self, text):
        text = str(text.decode('ascii', 'ignore'))
        text = text.lower()
        words = []
        for word in text.split():
            word = ''.join(c for c in word if c.isalpha())
            if word in self._words:
                words.append(word)
        return words

    @classmethod
    def from_path(cls, path):
        words = set()
        with open(path) as words_file:
            for line in words_file:
                line = line.strip()
                if line.isalpha():
                    words.add(line.lower())
        return cls(words)

