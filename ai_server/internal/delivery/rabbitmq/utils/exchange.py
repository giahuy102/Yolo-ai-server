from .exchange_type import ExchangeType
from .exchange_params import ExchangeParams

class Exchange:
    def __init__(self, name, typ=ExchangeType.DEFAULT, params=ExchangeParams()):
        self.name = name
        self.typ = typ
        self.params = params
