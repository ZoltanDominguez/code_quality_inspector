from pathlib import Path
from unittest.mock import Mock

import pytest
from starlette.testclient import TestClient

from cqi.app.coverage_router import coverage_router
from cqi.app.errors import ItemNotFoundInDatabase
from cqi.app.main import app
from cqi.db_connector.dynamodb import DBClient, DBSchemaNames, get_db_connector

APP_ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
DATA_FOLDER = APP_ROOT_DIR.joinpath("tests", "api_functional_tests", "data")
TEST_MAIN_COVERAGE_FILEPATH = DATA_FOLDER.joinpath("main_test_cov.xml")
EMPTY_COVERAGE_FILEPATH = DATA_FOLDER.joinpath("empty.xml")


@pytest.fixture(name="main_coverage")
def main_coverage_fixture():
    with open(TEST_MAIN_COVERAGE_FILEPATH, "r", encoding="utf-8") as f:
        yield f.read()


@pytest.fixture(name="empty_coverage")
def empty_coverage_fixture():
    with open(EMPTY_COVERAGE_FILEPATH, "r", encoding="utf-8") as f:
        yield f.read()


class MockDBClient:  # pylint: disable=too-few-public-methods
    def __init__(self):
        self.table = Mock(get_item=Mock())
        self.put_report = Mock()

    def get_report(self, project, branch):  # pylint: disable=unused-argument
        if "item_not_found" in branch:
            raise ItemNotFoundInDatabase

        return {
            DBSchemaNames.branch: branch,
            DBSchemaNames.project: project,
            DBSchemaNames.revision_hash: branch,
        }


@pytest.fixture(name="db_connector")
def db_connector_fixture():
    yield MockDBClient()


@pytest.fixture(name="fast_api_client")
def client_fixture(db_connector: DBClient):
    def get_db_override():
        return db_connector

    app.dependency_overrides[get_db_connector] = get_db_override
    app.include_router(coverage_router)

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
