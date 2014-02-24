# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import deque
import threading

import cherrypy

from tts.rapping.rap_composer import RapRenderer

__all__ = ['RapComposer']


class RapComposer(object):
    def __init__(self, dino_client, cleaner, rap_renderer):
        super(RapComposer, self).__init__()
        self._cleaner = cleaner
        self._dino_client = dino_client
        self._new_sms = threading.Condition()
        self._rap_renderer = rap_renderer
        self._sms_queue = deque()
        self._stop = threading.Event()
        self._subscribed = False

    def __enter__(self):
        if not self._subscribed:
            cherrypy.engine.subscribe('start', self._on_start)
            cherrypy.engine.subscribe('stop', self._on_stop)
            self._subscribed = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._subscribed:
            cherrypy.engine.unsubscribe('start', self._on_start)
            cherrypy.engine.unsubscribe('stop', self._on_stop)
            self._subscribed = False

    def _on_start(self):
        self._stop.clear()
        self._worker = threading.Thread(target=self._worker_loop,
                                        name='Rap composer')
        self._worker.start()

    def _on_stop(self):
        self._stop.set()
        with self._new_sms:
            self._new_sms.notify()
        self._worker.join()

    def _worker_loop(self):
        cherrypy.engine.publish('aquire_thread')
        while not self._stop.is_set():
            sms = None
            with self._new_sms:
                if self._sms_queue:
                    sms = self._sms_queue.popleft()
                else:
                    self._new_sms.wait()
            if sms is not None:
                self._add_lyrics(sms)
        cherrypy.engine.publish('release_thread')

    def _add_lyrics(self, sms):
        rr = self._rap_renderer
        if rr.has_enough_words():
            return
        self._dino_client.add_sms(sms)
        words = self._cleaner.clean(sms.message)
        rr.add_words(words)
        print(len(rr._words))
        if rr.has_enough_words():
            self._render_rap()

    def _render_rap(self):
        print('Rendering')
        rap_path = self._rap_renderer.render()
        print('Sending to dino')
        timed_words = self._rap_renderer.get_timed_words()
        self._dino_client.add_rap(rap_path, timed_words)

    def add_lryics(self, sms):
        with self._new_sms:
            self._sms_queue.append(sms)
            self._new_sms.notify()

