
from multiprocessing import Event
from .event_created_with_media_callback import EventCreatedWithMediaCallback

class CallbackContext:
    
    def get_event_callback(self, exchange_name, queue_name):
        if exchange_name == "event_processing" and queue_name == "event_created_with_media":
            return EventCreatedWithMediaCallback()
        return None
