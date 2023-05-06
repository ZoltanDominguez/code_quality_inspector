from pathlib import Path

from fastapi import FastAPI
from starlette.testclient import TestClient

from code_quality_inspector.app.coverage_router import coverage_router
from code_quality_inspector.app.endpoints import COVERAGE_ENDPOINT

APP_ROOT_DIR = Path(__file__).parent.parent.parent.resolve()


def test_ep_with_test_client():
    """Test stub using test client"""
    app = FastAPI(debug=False)
    app.include_router(coverage_router)
    fast_api_client = TestClient(app)

    response = fast_api_client.post(COVERAGE_ENDPOINT)
    print(response.json())
    expected_code = 200
    assert (
        response.status_code == expected_code
    ), f"Endpoint:{COVERAGE_ENDPOINT} not returned the {expected_code=}"
