
import concurrent.futures


# Singleton class
class WorkerProcessPool(object):

    def __init__(self):
        self.process_poll_excecutor = concurrent.futures.ProcessPoolExecutor(max_workers=4)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(WorkerProcessPool, cls).__new__(cls)
        return cls.instance

    def get_executor(self):
        return self.process_poll_excecutor
    
