import uuid
import time

class RandomGenerator:

    @staticmethod
    def gen_file_name(prefix=''):
        res = ''
        if prefix != '':
            res += '-'
        res = f'{res}{time.strftime("%Y%m%d-%H%M%S")}-{uuid.uuid4().hex}'
        return res
