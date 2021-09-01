import logging
import logging.handlers
import os
from sys import stdout

LOG_PATH = f"{os.path.abspath(os.path.dirname(__file__))}/std_out.log"


class Logger:
    def __init__(self, log_path: str = LOG_PATH, log_level: str = logging.INFO, file_enabled: bool = True, stdout_enabled: bool = True) -> None:
        self.log_path = log_path
        self.log_level = log_level
        self.file_enabled = file_enabled
        self.stdout_enabled = stdout_enabled

    def get_logger(self) -> logging.Logger:
        logger = logging.getLogger()
        logger.setLevel(self.log_level)
        format_str = "%(asctime)s [%(process)s] [%(levelname)s] [%(module)s] [%(funcName)s] %(message)s"
        formatter = logging.Formatter(format_str)

        if self.file_enabled:
            filer_handler = logging.FileHandler(
                self.log_path,
                encoding='utf-8'
            )
            filer_handler.setFormatter(formatter)
            logger.addHandler(filer_handler)

        if self.stdout_enabled:
            stream_handler = logging.StreamHandler(stdout)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

        if not self.file_enabled and not self.stdout_enabled:
            logger.addHandler(logging.NullHandler())
        return logger


if "LOGGER" not in globals():
    logger = Logger().get_logger()
