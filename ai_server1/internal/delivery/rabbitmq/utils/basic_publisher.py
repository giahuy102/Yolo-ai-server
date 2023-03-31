from .rabbitmq import RabbitMQ

class BasicPublisher(RabbitMQ):
    def __init__(self, exchange, queue):

        self.init_connection()
        self.init_channel()
        self.init_exchange(exchange.name, exchange.typ)
        self.init_queue(exchange.name, queue.name, queue.binding_keys, queue.params)

    def publish(self, exchange_name, routing_key, body):
        self.channel.basic_publish(exchange_name, routing_key, body)


