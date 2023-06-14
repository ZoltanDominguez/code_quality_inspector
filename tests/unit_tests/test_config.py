from cqi.config.config import read_config

from tests.testing_utils import UNIT_TEST_DATA_DIR

TEST_CONFIG_PATH = UNIT_TEST_DATA_DIR.joinpath("config_test.toml")


def test_read_config():
    config = read_config(str(TEST_CONFIG_PATH))
    assert config.main.log_level == "INFO"


def test_app_config_parse():
    _ = read_config()
