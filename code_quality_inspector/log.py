import logging

from code_quality_inspector.config.config import config

logging.basicConfig(level=config.main.log_level)


def get_logger(name: str):
    return logging.getLogger(name)
