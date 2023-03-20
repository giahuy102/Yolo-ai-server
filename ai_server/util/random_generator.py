import uuid
import time

class RandomGenerator:

    def gen_file_name(self, prefix=''):
        res = ''
        if prefix != '':
            res += '-'
        res = f'{res}{time.strftime("%Y%m%d-%H%M%S")}-{uuid.uuid4().hex}'
        return res
