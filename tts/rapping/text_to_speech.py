# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from xml.etree.ElementTree import Element, tostring

from tts.rapping.swift import Swift


class TextToSpeech(object):
    def __init__(self):
        self._swift =  Swift()

    def tts(self, wave_file, text, pitch=None, pitch_range=None, volume=None):
        attrib = {}
        if pitch is not None:
            attrib['pitch'] = '%sHz' % (pitch,)
        if pitch_range is not None:
            attrib['range'] = pitch_range

        prosody = Element('prosody', attrib=attrib)
        prosody.text = text

        ssml = tostring(prosody)
        self._swift.tts(wave_file, ssml, volume=volume)

