import pytest

from clientapi.auth import AuthBearer, InvalidTokenError


# Auth Scenarios
# Scenario 01: Creation Success
# Scenario 02: Missing Token
def test_bearer_token_creation_success(auth_token):
    # Given / When
    auth0_bearer = AuthBearer(auth_token)
    some_request = Request()
    auth0_bearer(some_request)

    # Then
    assert some_request.headers["Authorization"] == f"Bearer {auth_token}"


def test_missing_token():
    # Given / When
    with pytest.raises(InvalidTokenError):
        _ = AuthBearer(token=None)


@pytest.fixture
def auth_token():
    return "aRandomBearerTokenForAuth0Authentication"


class Request:
    headers: dict = {}
