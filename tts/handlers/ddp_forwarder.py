from tts.ddp import VisClient

class VisForwarder:
    def __init__(self, client):
        self._client = client

    def handle(self, sms):
        client.add_sms(sms)
        return sms

