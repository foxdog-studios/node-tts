from collections import namedtuple

import cherrypy
import random


REPLY = '%s. Now visit http://foxdogstudios.com'

REPLIES = [
    'Just in my pants - a moral position on underwear',
    'Company mission: end football now, do your part',
    'Our ideal holiday: cross dressing in Paris',
    'FDS believe in unlimited poppadoms',
    'V. plzd 2 announce FDS hd kidz, names are haddock, turbot and lemon sole',
    'Ask us about our binary finger counting course - HIGH 31!! hahaha..',
    'Buy a swan Pedalo and ride it pan-atlantic to Miami spring break 2015',
    'Why not try our battenburger: battenburg and burger',
    'Special deal on our clapping classes: $4,125 for 2 hours',
    'The Foxdog is an almost invincible creature its only weakness is poor'
    ' time management.'
]

_replies = []
for r in REPLIES:
   _replies.append(REPLY % (r,))
REPLIES = _replies

SmsMessage = namedtuple('SmsMessage', ('msg_id', 'number', 'message'))


class SmsServer:
    def __init__(self, incoming_sms_queue, host=None, port=None, reply=''):
        self._host = host
        self._port = port
        self._sms_queue = incoming_sms_queue
        self._replies = REPLIES
        self._msg_id = 0

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, message=None, number=None):
        self._sms_queue.put(SmsMessage(self._msg_id, number, message))
        self._msg_id += 1
        return [{'number' : number, 'message' : random.choice(self._replies)}]

    def mainloop(self):
        update = {
            'server.socket_host': self._host,
            'server.socket_port': self._port,
        }
        for key, value in update.items():
            if value is not None:
                cherrypy.config[key] = value
        cherrypy.quickstart(root=self, script_name='', config={'/': {}})

