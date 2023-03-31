from ...pkg.config.config import config

from ...entity.rabbitmq.exchange import Exchange
from ...entity.rabbitmq.queue import Queue 

from .utils.thread_consumer import ThreadConsumer

from .consumer_callbacks import ConsumerCallbacks

class Consumers:

    @staticmethod
    def consume_event_processing(callback=ConsumerCallbacks.calback_event_processing):
        broker_config = config['rabbitmq']
        consumers = list()
        exchanges = broker_config["exchanges"]
        for ex in exchanges:
            if ex["name"] == "event_processing":
                exchange = ex
                break
        new_exchange = Exchange(exchange["name"])
        for q in exchange["queues"]:
            if q["name"] == "event_created_with_media":
                new_queue = Queue(q["name"], q["binding_keys"])
                consumer = ThreadConsumer(new_exchange, new_queue, callback)
                consumers.append(consumer)
                consumer.start()







