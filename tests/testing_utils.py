from pathlib import Path

TESTS_ROOT_DIR = Path(__file__).parent.resolve()
UNIT_TEST_DATA_DIR = TESTS_ROOT_DIR.joinpath("unit_tests", "data")
API_TEST_DATA_DIR = TESTS_ROOT_DIR.joinpath("api_functional_tests", "data")
