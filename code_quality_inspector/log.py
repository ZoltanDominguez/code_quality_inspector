import logging

from code_quality_inspector.config.config import config

logging.basicConfig(
    format="%(levelname)-9s %(module)s: %(message)s",
    level=config.main.log_level,
)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
