from base64 import b64encode

from requests import Session
from requests.auth import AuthBase, HTTPBasicAuth

from clientapi import sessions
from clientapi.auth import Bearer, SharedSecret


# Scenarios for sessions
# Scenario 01: no_auth
# Scenario 02: bearer
# Scenario 03: secret key
# Scenario 04: basic
def test_sessions_no_auth():
    # When
    with sessions.no_auth() as s:
        # Then
        assert isinstance(s, Session)


def test_sessions_bearer():
    # Given
    token = "some_token"

    # When
    with sessions.bearer(token) as s:
        # Then
        assert isinstance(s, Session)
        assert isinstance(s.auth, Bearer)

        dummy_request = DummyRequest()
        s.auth(dummy_request)
        assert dummy_request.headers["Authorization"] == f"Bearer {token}"


def test_sessions_shared_secret_key():
    # Given
    shared_secret = "some_key"

    # When
    with sessions.shared_secret(shared_secret) as s:
        # Then
        assert isinstance(s, Session)
        assert isinstance(s.auth, SharedSecret)

        dummy_request = DummyRequest()
        s.auth(dummy_request)
        assert dummy_request.headers["SHARED_SECRET"] == shared_secret


def test_sessions_basic():
    # Given
    username = "test_username"
    password = "test_password"

    # When
    with sessions.basic(username, password) as s:
        # Then
        assert isinstance(s, Session)
        assert isinstance(s.auth, HTTPBasicAuth)

        dummy_request = DummyRequest()
        s.auth(dummy_request)

        expected_basic_token = _get_expected_basic_token(username, password)
        assert dummy_request.headers["Authorization"] == f"Basic {expected_basic_token}"


def test_sessions_base():
    # Given
    auth_base = AuthBase()

    # When
    with sessions.base(auth_base) as s:
        # Then
        assert isinstance(s, Session)
        assert isinstance(s.auth, AuthBase)


def _get_expected_basic_token(username, password):
    basic_str = f"{username}:{password}"
    return b64encode(basic_str.encode()).decode()


class DummyRequest:
    headers: dict = {}
