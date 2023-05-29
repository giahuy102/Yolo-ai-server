from logging import getLogger, getLevelName, Formatter, StreamHandler, FileHandler
from pathlib import Path

def set_logger():
    log_formatter = Formatter("%(asctime)s [%(levelname)s]: %(message)s [%(processName)s] [%(threadName)s]")


    logger = getLogger()
    logger.setLevel(getLevelName('INFO'))

    # log_path = Path(__file__).parents[2] / 'logs' / 'server.log'
    # file_handler = FileHandler(log_path)
    # file_handler.setFormatter(log_formatter)
    # logger.addHandler(file_handler)

    console_handler = StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)
