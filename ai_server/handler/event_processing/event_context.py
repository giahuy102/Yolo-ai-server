# Strategy design pattern

class EventContext:
    def __init__(self):
        self.handler = None

    def execute_handler(self, event, typ):
        self.handler.execute(event, typ)

    def set_handler(self, handler):
        self.handler = handler
        