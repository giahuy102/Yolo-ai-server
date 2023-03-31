from enum import Enum

class ExchangeType(Enum):
    DEFAULT = 'topic'
    DIRECT = 'direct'
    FANOUT = 'fanout'
    TOPIC = 'topic'
    HEADER = 'header'
