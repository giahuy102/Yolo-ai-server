import threading

from ....pkg.config.config import config
from ..rabbitmq.producer import Producer
from ..rabbitmq.utils.exchange import Exchange
from ..rabbitmq.utils.queue import Queue
from ...handler.stream_event_detection.stream_event_detector import StreamEventDetector
from ...handler.stream_event_detection.utils.stream_event_input import StreamEventInput

from ...grpc_client.camera_stream_info_handler import CameraStreamHandler
from ..utils.stream_utils import StreamUtils

BROKER_CONFIG = config["rabbitmq"]
EXCHANGES = BROKER_CONFIG["exchanges"]
EVENT_CONFIG = config["event"]
IOT_EVENT = EVENT_CONFIG["iot"]
CAMERA_EVENT = EVENT_CONFIG["camera"]

class StreamDetector:

    def callback_event_output(self, event_output):
        event_key = event_output.event_key
        json_event_output = event_output.to_json()
        exchange = EXCHANGES["stream_processing"]
        queue = exchange["queues"]["camera_event_new"]
        event_key_prefix = queue["routing_key_prefix"]["event_new_camera"]
        routing_key = f"{event_key_prefix}.{event_key}"
        arg_exchange = Exchange(exchange["name"])
        arg_queue = Queue(queue["name"], queue["binding_keys"])


        # print("$$$$$$$$$")
        # print(json_event_output)
        # print(event_key_prefix)
        # print(routing_key)

        producer = Producer(arg_exchange, arg_queue)
        producer.produce_message(routing_key, json_event_output)

    def start_detector(self):
        stream_infos = list()
        stream_utils = StreamUtils()
        handler = CameraStreamHandler()
        camera_streams = handler.get_all_camera_streams()
        for camera in camera_streams:
            stream_infos.append(stream_utils.parse_stream_info(camera))

        stream_event_input = StreamEventInput(stream_infos)
        stream_event_detector = StreamEventDetector()
        stream_event_detector.execute(stream_event_input, self.callback_event_output)


    def start(self):
        detector_thread = threading.Thread(target=self.start_detector)
        detector_thread.start()
        return detector_thread
        



