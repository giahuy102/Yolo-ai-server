from ...pkg.config.config import config

from ...entity.rabbitmq.exchange import Exchange
from ...entity.rabbitmq.queue import Queue 

from .util.thread_consumer import ThreadConsumer

from .consumer_callbacks import ConsumerCallbacks

class Consumers:

    @staticmethod
    def consume_event_processing(callback=ConsumerCallbacks.calback_event_processing):
        broker_config = config['rabbitmq']
        consumers = list()
        exchange = broker_config["exchanges"]["event_processing"]
        new_exchange = Exchange(exchange["name"])
        for q in exchange["queues"]:
            new_queue = Queue(q["name"], q["binding_keys"])
            consumer = ThreadConsumer(new_exchange, new_queue, callback)
            consumers.append(consumer)
            consumer.start()







