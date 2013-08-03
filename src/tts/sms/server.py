from collections import namedtuple

import cherrypy


SmsMessage = namedtuple('SmsMessage', ('msg_id', 'number', 'message'))


class SmsServer:
    def __init__(self, incoming_sms_queue, host=None, port=None, reply=''):
        self._host = host
        self._port = port
        self._sms_queue = incoming_sms_queue
        self._reply = reply
        self._msg_id = 0

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, message=None, number=None):
        self._sms_queue.put(SmsMessage(self._msg_id, number, message))
        self._msg_id += 1
        return [{'number' : number, 'message' : self._reply}]

    def mainloop(self):
        update = {
            'server.socket_host': self._host,
            'server.socket_port': self._port,
        }
        for key, value in update.items():
            if value is not None:
                cherry.config[key] = value
        cherrypy.quickstart(root=self, script_name='', config={'/': {}})

