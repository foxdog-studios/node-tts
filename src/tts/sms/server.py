import cherrypy

from tts.messages import Message


class SmsServer:
    def __init__(self, handler, host=None, port=None):
        self._handler = handler
        self._host = host
        self._port = port

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, message=None, number=None):
        message = Message(message, number=number)
        reply = self._handler.handle(message)
        return [] if reply is None else [reply]

    def serve(self):
        update = {'server.socket_host': self._host,
                  'server.socket_port': self._port}
        for key, value in update.items():
            if value is not None:
                cherrypy.config[key] = value
        cherrypy.quickstart(root=self, script_name='', config={'/': {}})

