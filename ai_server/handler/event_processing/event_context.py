# Strategy design pattern

class EventContext:
    def __init__(self):
        self.handler = None

    def execute_handler(self, event_input, typ):
        if typ == "video":
            self.handler.execute_video(event_input)

    def set_handler(self, handler):
        self.handler = handler
        