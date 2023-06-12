import pika

from .....pkg.config.config import config


# Set the connection parameters to connect to rabbit-server1 on port 5672
# on the / virtual host using the username "guest" and password "guest"
BROKER_CONFIG = config["rabbitmq"]
USERNAME = BROKER_CONFIG["username"]
PASSWORD = BROKER_CONFIG["password"]
HOST = BROKER_CONFIG["host"]
PORT = BROKER_CONFIG["port"]
VIRTUAL_HOST = BROKER_CONFIG["virtual_host"]



class RabbitMQConnection:
    def __init__(self, username=USERNAME, password=PASSWORD, host=HOST, port=PORT, virtual_host=VIRTUAL_HOST):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.virtual_host = virtual_host

        

    def init(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(self.host, self.port, self.virtual_host, credentials)
        self.connnection = pika.BlockingConnection(parameters)
        return self.connnection

    def get_connection(self):
        return self.connection



