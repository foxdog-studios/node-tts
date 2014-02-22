# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


def count(iterable, predicate):
    return sum(1 for item in iterable if predicate(item))

def format_obj(template, obj):
    return template.format(**obj.__dict__)

