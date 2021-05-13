import pytest

from clientapi.auth import (
    Bearer,
    BearerTokenNotValid,
    SharedSecret,
    SharedSecretKeyNotValid,
)


# Bearer Scenarios
# Scenario 01: Creation Success
# Scenario 02: Missing Token
def test_bearer_token_creation_success(auth_token):
    # Given / When
    auth_bearer = Bearer(auth_token)
    some_request = Request()
    auth_bearer(some_request)

    # Then
    assert some_request.headers["Authorization"] == f"Bearer {auth_token}"


def test_missing_token():
    # Given / When
    with pytest.raises(BearerTokenNotValid):
        _ = Bearer(token=None)


# SharedSecret Scenarios
# Scenario 01: Creation Success
# Scenario 02: Missing Key
def test_shared_secret_creation_success(shared_secret_key):
    # Given / When
    shared_secret = SharedSecret(shared_secret_key)
    some_request = Request()
    shared_secret(some_request)

    # Then
    assert some_request.headers["SHARED_SECRET"] == shared_secret_key


def test_shared_secret_missing_key():
    # Given / When
    with pytest.raises(SharedSecretKeyNotValid):
        _ = SharedSecret(key=None)


@pytest.fixture(name="auth_token")
def get_auth_token():
    return "aRandomBearerTokenForAuthentication"


@pytest.fixture(name="shared_secret_key")
def get_shared_secret_key():
    return "aRandomSharedSecretKey"


class Request:
    headers: dict = {}
