import random

import cherrypy

from tts.message import Message


class SmsServer:
    def __init__(self, incoming_sms_queue, host=None, port=None, replies=None):
        assert replies, 'Currently, at least one reply must be given'
        self._host = host
        self._port = port
        self._sms_queue = incoming_sms_queue
        self._replies = replies

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, message=None, number=None):
        if message is None or number is None:
            return
        message = Message(number, message)
        self._sms_queue.put(message)
        return [{'number': number, 'message': random.choice(self._replies)}]

    def serve(self):
        update = {
            'server.socket_host': self._host,
            'server.socket_port': self._port,
        }
        for key, value in update.items():
            if value is not None:
                cherrypy.config[key] = value
        cherrypy.quickstart(root=self, script_name='', config={'/': {}})

