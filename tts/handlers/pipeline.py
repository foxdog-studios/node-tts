class PipelineHandler:
    def __init__(self, stages):
        self._stages = stages

    def handle(self, sms):
        reply = sms
        for stage in self._stages:
            reply = stage.handle(reply)
        return reply

