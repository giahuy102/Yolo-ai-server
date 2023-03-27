from .rabbitmq_connection import RabbitMQConnection


class RabbitMQ:

    def init_connection(self):
        self.connection = RabbitMQConnection().init()

    def init_channel(self):
        self.channel = self.connection.channel()

    def init_exchange(self, exchange, exchange_type):
        self.channel.exchange_declare(exchange, exchange_type)
        

    def init_queue(self, exchange_name, queue_name, binding_keys, queue_params):
        self.channel.queue_declare(queue=queue_name, durable=queue_params.durable)
        for binding_key in binding_keys:
            self.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=binding_key)
