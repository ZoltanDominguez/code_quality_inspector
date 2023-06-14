from pathlib import Path

import tomli
from pydantic import BaseModel, Field

CONFIG_DIRECTORY = Path(__file__).parent.resolve()
CONFIG_PATH = CONFIG_DIRECTORY.joinpath("config.toml")
DEFAULT_LOG_LEVEL = "INFO"


class MainConfig(BaseModel):
    log_level: str = Field(default=DEFAULT_LOG_LEVEL)


class DBConfig(BaseModel):
    table_name: str


class Config(BaseModel):
    main: MainConfig
    db: DBConfig


def read_config(config_path: str = str(CONFIG_PATH)) -> Config:
    with open(config_path, "rb") as f:
        toml_dict = tomli.load(f)
        return Config.parse_obj(toml_dict)


config = read_config()
