import json
import logging
import threading
import functools

from ....pkg.config.config import config
from ..rabbitmq.producer import Producer
from ..rabbitmq.utils.exchange import Exchange
from ..rabbitmq.utils.queue import Queue
from ...handler.video_event_processing.utils.video_event_input import VideoEventInput
from ...handler.video_event_processing.video_event_processor import VideoEventProcessor

BROKER_CONFIG = config["rabbitmq"]
EXCHANGES = BROKER_CONFIG["exchanges"]
EVENT_CONFIG = config["event"]
IOT_EVENT = EVENT_CONFIG["iot"]
CAMERA_EVENT = EVENT_CONFIG["camera"]

class EventCreatedWithMediaCallback:

    def parse_event_input(self, json_body):
        event_id = json_body["_id"]
        event_key = json_body["event_key"]
        video_url = json_body["normal_video_url"]
        start_time = json_body["start_time"]
        end_time = json_body["end_time"]
        target_time = json_body["event_time"]

        iot_event_zone_coords = json_body["iot_event_zone_coords"] if json_body.get("iot_event_zone_coords") else []
        camera_event_zone_coords = json_body["camera_event_zone_coords"] if json_body.get("camera_event_zone_coords") else []

        image_url = json_body["normal_image_url"] if json_body.get("normal_image_url") else None
        detection_image_url = json_body["detection_image_url"] if json_body.get("detection_image_url") else None
        line_coords = json_body["line_coords"] if json_body.get("line_coords") != None and type(json_body.get("line_coords")) is list and len(json_body.get("line_coords")) > 1 else None

        line_crossing_vector = json_body["line_crossing_vector"] if json_body.get("line_crossing_vector") and type(json_body.get("line_crossing_vector")) is list and len(json_body.get("line_crossing_vector")) > 3 else None

        return VideoEventInput(event_id, event_key, video_url, start_time, end_time, target_time, iot_event_zone_coords, camera_event_zone_coords, detection_image_url, image_url, line_coords, line_crossing_vector)

    def valid_event_input(self, event_input):
        if event_input.event_key == CAMERA_EVENT["line_crossing"]["key"]:
            if not event_input.line_coords:
                return False
        return True

    def get_event_key_prefix(self, queue, is_ai_event):
        if is_ai_event:
            return queue["routing_key_prefix"]["event_verified_camera"]
        else:
            return queue["routing_key_prefix"]["event_verified_iot"]

    def callback_event_output(self, event_key, event_output):
        json_event_output = event_output.to_json()
        exchange = EXCHANGES["event_processing"]
        queue = exchange["queues"]["event_verified"]
        event_key_prefix = self.get_event_key_prefix(queue, event_output.is_ai_event)
        routing_key = f"{event_key_prefix}.{event_key}"
        arg_exchange = Exchange(exchange["name"])
        arg_queue = Queue(queue["name"], queue["binding_keys"])

        producer = Producer(arg_exchange, arg_queue)
        producer.produce_message(routing_key, json_event_output)


        

    def execute(self, channel, method, properties, body):
        # routing_key = method.routing_key.split('.')
        # event_key = routing_key[-1]
        json_body = json.loads(body)
        event_input = self.parse_event_input(json_body)

        if not self.valid_event_input(event_input):
            return

        video_event_processor = VideoEventProcessor()
        logging.info("Handle detection video in new thread")
        thread = threading.Thread(target=video_event_processor.execute, args=(event_input, functools.partial(self.callback_event_output, event_input.event_key)))
        thread.start()
        # video_event_processor.execute(event_input, self.callback_event_output(event_input.event_key))

