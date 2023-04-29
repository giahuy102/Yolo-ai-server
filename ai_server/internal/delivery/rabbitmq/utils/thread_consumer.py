import threading

# from .rabbitmq_connection import RabbitMQConnection
from .rabbitmq import RabbitMQ

class ThreadConsumer(threading.Thread, RabbitMQ):

    """
        Declare one channel
        Declare one exchange for that channel (Although we can also declare multiple exchanges for one channel)
        Declare one queue for that exchange (Although we can also declare multiple queue for one exchange)

        This consumer just handles for one queue - one exchange - one channel
    """

    def __init__(self, exchange, queue, callback):
        # super().__init__()
        threading.Thread.__init__(self)
        # self.connection = RabbitMQConnection().init()

        
        self.init_connection()
        self.init_channel()
        self.init_exchange(exchange.name, exchange.typ, exchange.params)
        self.init_queue(exchange.name, queue.name, queue.binding_keys, queue.params)

        # Temporarily add auto ack for message
        self.channel.basic_consume(queue=queue.name, auto_ack=True, on_message_callback=callback)



    # def init_channel(self):
    #     self.channel = self.connection.channel()

    # def init_exchange(self, exchange, exchange_type):
    #     self.channel.exchange_declare(exchange, exchange_type)
        

    # def init_queue(self, exchange_name, queue_name, binding_keys, queue_params):
    #     self.channel.queue_declare(queue=queue_name, durable=queue_params.durable)
    #     for binding_key in binding_keys:
    #         self.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=binding_key)


    def run(self):
        self.channel.start_consuming()

