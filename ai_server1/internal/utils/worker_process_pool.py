
import concurrent.futures


# Singleton class
class WorkerProcessPool:
    """
        This singleton object don't need thread-safe because it's currently only be used in 1 thread
    """

    _instance = None

    def __init__(self):
        if WorkerProcessPool._instance != None:
            raise Exception("This class is a singleton! Please access from get_instance method")
        WorkerProcessPool._instance = self
        self.process_pool_excecutor = concurrent.futures.ProcessPoolExecutor(max_workers=4)

    def get_executor(self):
        return self.process_pool_excecutor

    @staticmethod
    def get_instance():
        if WorkerProcessPool._instance == None:
            WorkerProcessPool()
        return WorkerProcessPool._instance
