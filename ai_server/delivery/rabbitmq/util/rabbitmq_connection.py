import pika

from ...pkg.config.config import config


# Set the connection parameters to connect to rabbit-server1 on port 5672
# on the / virtual host using the username "guest" and password "guest"
broker_config = config["rabbitmq"]


class RabbitMQConnection:
    def __init__(self, username=broker_config["username"], password=broker_config["password"], host=broker_config["host"], port=broker_config["port"], virtual_host=broker_config["virtual_host"]):
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



