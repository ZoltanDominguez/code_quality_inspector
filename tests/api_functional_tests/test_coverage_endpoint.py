import pytest

from cqi.app.endpoints import COVERAGE_ENDPOINT
from cqi.app.errors import FileIsEmpty
from tests.common_asserts import assert_status_code

GIT_HASH = "test_git_hash_12345"
GIT_BRANCH = "main"
PROJECT_NAME = "cqi_tests"


@pytest.fixture(name="main_coverage_report_to_db")
def main_coverage_report_to_db_fixture():
    return {
        "revision_hash": GIT_HASH,
        "branch_name": GIT_BRANCH,
        "project_name": PROJECT_NAME,
        "coverage": {
            "data": {
                "unittest": {
                    "overall_branch_coverage": {
                        "coverage": 19.23,
                        "valid": 26,
                        "covered": 5,
                    },
                    "overall_line_coverage": {
                        "coverage": 35.76,
                        "valid": 151,
                        "covered": 54,
                    },
                    "coverages_per_file": {
                        "log.py": {
                            "filename": "log.py",
                            "line_rate": 100.0,
                            "branch_rate": 100.0,
                        },
                        "app/coverage_router.py": {
                            "filename": "app/coverage_router.py",
                            "line_rate": 100.0,
                            "branch_rate": 100.0,
                        },
                        "github_connector/comment_to_pr.py": {
                            "filename": "github_connector/comment_to_pr.py",
                            "line_rate": 41.38,
                            "branch_rate": 20.0,
                        },
                        "github_connector/github_init.py": {
                            "filename": "github_connector/github_init.py",
                            "line_rate": 100.0,
                            "branch_rate": 50.0,
                        },
                        "github_connector/github_utils.py": {
                            "filename": "github_connector/github_utils.py",
                            "line_rate": 53.85,
                            "branch_rate": 100.0,
                        },
                    },
                },
            }
        },
    }


def test_ep_with_test_client(
    db_connector, fast_api_client, main_coverage, main_coverage_report_to_db
):
    data = {
        "revision_hash": GIT_HASH,
        "branch": GIT_BRANCH,
    }
    url = COVERAGE_ENDPOINT + f"/{PROJECT_NAME}/unittest"
    response = fast_api_client.post(url=url, data=data, files={"file": main_coverage})
    assert_status_code(response=response, expected_code=204)
    db_connector.put_report.assert_called_with(report=main_coverage_report_to_db)


def test_no_file_present(fast_api_client, empty_coverage):
    data = {
        "revision_hash": GIT_HASH,
        "branch": GIT_BRANCH,
    }
    url = COVERAGE_ENDPOINT + f"/{PROJECT_NAME}/unittest"
    response = fast_api_client.post(url=url, data=data, files={"file": empty_coverage})
    assert_status_code(response=response, expected_code=422)

    assert response.json() == FileIsEmpty.api_error


def test_item_not_found(
    db_connector, fast_api_client, main_coverage, main_coverage_report_to_db
):
    branch_name = "item_not_found_test_branch"
    data = {
        "revision_hash": GIT_HASH,
        "branch": branch_name,
    }
    url = COVERAGE_ENDPOINT + f"/{PROJECT_NAME}/unittest"
    response = fast_api_client.post(url=url, data=data, files={"file": main_coverage})
    assert_status_code(response=response, expected_code=204)

    main_coverage_report_to_db["branch_name"] = branch_name
    db_connector.put_report.assert_called_with(report=main_coverage_report_to_db)
