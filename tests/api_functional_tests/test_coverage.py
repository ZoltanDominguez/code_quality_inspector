from pathlib import Path

APP_ROOT_DIR = Path(__file__).parent.parent.parent.resolve()


def test_ep_with_test_client():
    """Test stub using test client"""
    '''app = FastAPI(debug=False)
    app.include_router(coverage_router)
    fast_api_client = TestClient(app)

    response = fast_api_client.post(COVERAGE_ENDPOINT)
    print(response.json())
    expected_code = 200
    assert (
        response.status_code == expected_code
    ), f"Endpoint:{COVERAGE_ENDPOINT} not returned the {expected_code=}"'''
