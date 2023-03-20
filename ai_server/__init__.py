from flask import Flask
app = Flask(__name__)


# from pathlib import Path
# print(Path(__file__).parent)

# (Path(__file__).parent / 'static1' / 'test').mkdir(parents=True, exist_ok=True)

# @app.route('/')
# def hello_world():
#    return 'Hello world'









from .pkg.config.config import config

from .entity.rabbitmq.exchange import Exchange
from .entity.rabbitmq.queue import Queue 

from .delivery.rabbitmq.thread_consumer import ThreadConsumer


def callback(channel, method, properties, body):
   print(method.routing_key)


broker_config = config['rabbitmq']

consumers = list()



for exchange in broker_config['exchanges']:
   new_exchange = Exchange(exchange["name"])
   for q in exchange["queues"]:
      new_queue = Queue(q["name"], q["binding_keys"])
      consumer = ThreadConsumer(new_exchange, new_queue, callback)
      consumers.append(consumer)
      consumer.start()







