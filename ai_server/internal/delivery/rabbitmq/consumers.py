from ....pkg.config.config import config

from .utils.exchange import Exchange
from .utils.queue import Queue 
from .utils.thread_consumer import ThreadConsumer
from .callback_context import CallbackContext

BROKER_CONFIG = config["rabbitmq"]
EXCHANGES = BROKER_CONFIG["exchanges"]


class Consumers:

    def __init__(self):
        self.consumers = list()

    def start(self):
        callback_context = CallbackContext()
        exchange = EXCHANGES["event_processing"]
        queue = exchange["queues"]["event_created_with_media"]

        exchange_name = exchange["name"]
        queue_name = queue["name"]
        queue_binding_keys = queue["binding_keys"]
        callback_obj = callback_context.get_event_callback(exchange_name, queue_name)

        if callback_obj:
            arg_exchange = Exchange(exchange_name)
            arg_queue = Queue(queue_name, queue_binding_keys)
            consumer = ThreadConsumer(arg_exchange, arg_queue, callback_obj.execute)
            self.consumers.append(consumer)
            consumer.start()


        # for exchange in self.exchanges:
        #     exchange_name = self.exchanges[exchange]["name"]
        #     queues = self.exchanges[exchange]
        #     for queue in queues:
        #         queue_name = queues[queue]["name"]
        #         queue_binding_keys = queues[queue]["binding_keys"]
        #         callback_obj = callback_context.get_event_callback(exchange_name, queue_name)
        #         if callback_obj:
        #             arg_exchange = Exchange(exchange_name)
        #             arg_queue = Queue(queue_name, queue_binding_keys)
        #             consumer = ThreadConsumer(arg_exchange, arg_queue, callback_obj.execute)
        #             self.consumers.append(consumer)
        #             consumer.start()


    # @staticmethod
    # def consume_event_processing(callback=ConsumerCallbacks.calback_event_processing):
    #     broker_config = config['rabbitmq']
    #     consumers = list()
    #     exchanges = broker_config["exchanges"]
    #     for ex in exchanges:
    #         if ex["name"] == "event_processing":
    #             exchange = ex
    #             break
    #     new_exchange = Exchange(exchange["name"])
    #     for q in exchange["queues"]:
    #         if q["name"] == "event_created_with_media":
    #             new_queue = Queue(q["name"], q["binding_keys"])
    #             consumer = ThreadConsumer(new_exchange, new_queue, callback)
    #             consumers.append(consumer)
    #             consumer.start()







