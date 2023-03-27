from ...pkg.config.config import config

import json



from ...handler.event_processing.event_context import EventContext
from ...handler.event_processing.object_detected import ObjectDetected
from ...entity.event.event_processing.event_processing_input import EventProcessingInput

from ...util.worker_process_pool import WorkerProcessPool

class ConsumerCallbacks:

    @staticmethod
    def calback_event_processing(channel, method, properties, body):
        
        broker_config = config['rabbitmq']
        event_config = config["event"]
        iot_config = event_config["iot"]
        camera_config = event_config["camera"]

        for ex in broker_config["exchanges"]:
            if ex["name"] == "event_processing":
                exchange = ex
                break
        routing_key = method.routing_key.split('.')

        body = json.loads(body)

        event_context = EventContext()

        print(body)

        event_input = EventProcessingInput(body["event_id"], body["video_url"], body["start_time"], body["end_time"], body["target_time"])


        if routing_key[-1] == iot_config["movement"]["key"]:
            handler = ObjectDetected()
            event_context.set_handler(handler)
            
            pool_executor = WorkerProcessPool().get_executor()
            pool_executor.submit(event_context.execute_handler, event_input, "video")


