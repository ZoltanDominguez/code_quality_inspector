from pathlib import Path

import tomli
from pydantic import BaseModel

CONFIG_DIRECTORY = Path(__file__).parent.resolve()
CONFIG_PATH = CONFIG_DIRECTORY.joinpath("config.toml")


class MainConfig(BaseModel):
    log_level: str


class Config(BaseModel):
    main: MainConfig


def read_config(config_path: str = str(CONFIG_PATH)):
    with open(config_path, "rb") as f:
        toml_dict = tomli.load(f)
        return Config.parse_obj(toml_dict)


config = read_config()
