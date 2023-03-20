from .exchange_type import ExchangeType

class Exchange:
    def __init__(self, name, typ=ExchangeType.DEFAULT):
        self.name = name
        self.typ = typ
