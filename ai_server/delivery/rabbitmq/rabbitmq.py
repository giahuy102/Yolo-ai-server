import queue
import pika
import threading

from .exchange_type import ExchangeType
from .queue_params import QueueParams

class RabbitMQ:

    def __init__(self, host='localhost', queue_params=QueueParams):
        self.consumers = set()
        
        self.conn = None
        self.queue_params = queue_params


        self.init_connection(host)

    def init_connection(self, host):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=host))


    def add_new_consumer(self, exchange, exchange_type, queue_name, binding_keys, callback, auto_ack):
        channel = self.add_new_channel(exchange, exchange_type)

        channel.queue_declare(queue=queue_name, durable=self.queue_params.durable)

        for binding_key in binding_keys:
            channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=binding_key)

        
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=auto_ack)
        

        



    def add_new_channel(self, exchange, exchange_type):
        conn = self.get_connection()
        channel = conn.channel()
        channel.exchange_declare(exchange, exchange_type)
        
        return channel
        

    def get_connection(self):
        return self.conn



