from flask import Flask
app = Flask(__name__)


# from pathlib import Path
# print(Path(__file__).parent)

# (Path(__file__).parent / 'static1' / 'test').mkdir(parents=True, exist_ok=True)

# @app.route('/')
# def hello_world():
#    return 'Hello world'




from .delivery.rabbitmq.consumers import Consumers

from .handler.rtsp_stream.stream_loader import StreamLoader
from .entity.rtsp_stream.rtsp_stream import RTSPStream
from .handler.event_processing.object_detected import ObjectDetected
from .handler.object_detection.yolov7.object_detector import ObjectDetector
from .handler.object_detection.yolov7.detection_stream import DetectionStream

def main():


    # import cv2
    # import numpy as np
    

    # frameSize = (600, 500)

    # out = cv2.VideoWriter('/home/legiahuy/HK222/DATN/Ai/yolo_ai_server/ai_server/static/detection/video/out.mp4',cv2.VideoWriter_fourcc(*'H264'), 60, frameSize)

    # for i in range(0,255):
    #     img = np.ones((500, 600, 3), dtype=np.uint8)*i
    #     out.write(img)
    # print(img.shape)

    # out.release()










    Consumers.consume_event_processing()
    
    # Initial data - Only use for testing
    # stream_info = RTSPStream("test_camera_id", "rtsp://admin:Dientoan@123@tris.ddns.net:5564/Streaming/Channels/102?transportmode=unicast&profile=Profile_2", "movement")
    # stream_loader = StreamLoader([stream_info])
    # detection_stream = DetectionStream(stream_loader)

      
    # detected_handler = ObjectDetected()
    # detector = ObjectDetector()
    # detector.detect(detection_stream, detected_handler.callback_stream)



main()





# from .entity.event.event_processing.event_processing_input import EventProcessingInput
# from .handler.event_processing.event_context import EventContext
# from .handler.event_processing.object_detected import ObjectDetected

# handler = ObjectDetected()
# ctx = EventContext()
# ctx.set_handler(handler)

# event_input = EventProcessingInput("id_1", "http://localhost:5001/static/test/test_video.mp4", "2023-03-25T08:35:00", "2023-03-25T08:35:13", "2023-03-25T08:35:02")
# ctx.execute_handler(event_input, "video")



# from .pkg.config.config import config

# from .entity.rabbitmq.exchange import Exchange
# from .entity.rabbitmq.queue import Queue 

# from .delivery.rabbitmq.thread_consumer import ThreadConsumer


# def callback(channel, method, properties, body):
#    print(method.routing_key)


# broker_config = config['rabbitmq']

# consumers = list()



# for exchange in broker_config['exchanges']:
#    new_exchange = Exchange(exchange["name"])
#    for q in exchange["queues"]:
#       new_queue = Queue(q["name"], q["binding_keys"])
#       consumer = ThreadConsumer(new_exchange, new_queue, callback)
#       consumers.append(consumer)
#       consumer.start()







