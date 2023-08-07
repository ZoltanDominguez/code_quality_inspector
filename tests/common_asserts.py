from requests import Response


def assert_status_code(response: Response, expected_code: int):
    assert response.status_code == expected_code, (
        f"Wrong status code for {response.url}. "
        f"{response.status_code=} {expected_code=}"
    )
