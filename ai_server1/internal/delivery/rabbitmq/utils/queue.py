from .queue_params import QueueParams

class Queue:
    def __init__(self, name, binding_keys, params=QueueParams()):
        self.name = name
        self.binding_keys = binding_keys
        self.params = params
