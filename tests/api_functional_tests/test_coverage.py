from code_quality_inspector.app.endpoints import COVERAGE_ENDPOINT

GIT_HASH = "test_git_hash_12345"
GIT_BRANCH = "main"


def test_ep_with_test_client(fast_api_client, main_coverage):
    """Test stub using test client"""
    data = {
        "revision_hash": GIT_HASH,
        "branch": GIT_BRANCH,
    }
    url = COVERAGE_ENDPOINT + "/testproject/unittest"
    response = fast_api_client.post(url=url, data=data, files={"file": main_coverage})
    print(response.json())
    expected_code = 200
    assert (
        response.status_code == expected_code
    ), f"Endpoint:{COVERAGE_ENDPOINT} not returned the {expected_code=}"
