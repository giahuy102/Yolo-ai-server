from flask import Flask
app = Flask(__name__)


# from pathlib import Path
# print(Path(__file__).parent)

# (Path(__file__).parent / 'static1' / 'test').mkdir(parents=True, exist_ok=True)

# @app.route('/')
# def hello_world():
#    return 'Hello world'




from .delivery.rabbitmq.consumers import Consumers

def main():
    Consumers.consume_event_processing()
    






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







