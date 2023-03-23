from ...pkg.config.config import config

import json



from ...handler.event_processing.event_context import EventContext

class ConsumerCallbacks:

    @staticmethod
    def calback_event_processing(channel, method, properties, body):
        
        broker_config = config['rabbitmq']
        event_config = config["event"]
        iot_config = event_config["iot"]
        camera_config = event_config["camera"]

        exchange = broker_config["exchanges"]["event_processing"]
        routing_key = method.routing_key.split('.')

        body = json.loads(body)

        event_context = EventContext()


        if routing_key[-1] == iot_config["door_open"]["key"]:
            


