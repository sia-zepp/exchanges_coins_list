import logging

class Logger:

    log_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    def __init__(self, log_levels=log_levels):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_levels['INFO'])
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler('app_logs.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.propagate = False

    def set_log_level(self, level):
        self.logger.setLevel(level)

logger = Logger()