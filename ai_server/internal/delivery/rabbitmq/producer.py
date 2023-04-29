from .utils.basic_publisher import BasicPublisher


class Producer:
    def __init__(self, exchange, queue):
        self.publisher = BasicPublisher(exchange, queue)

    def produce_message(self, routing_key, body):
        self.publisher.publish(routing_key, body)
