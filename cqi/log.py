import logging

from cqi.config.config import app_config

logging.basicConfig(
    format="%(levelname)-9s %(module)s: %(message)s",
    level=app_config.main.log_level,
)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
