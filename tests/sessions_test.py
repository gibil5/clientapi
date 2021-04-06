from requests import Session

from clientapi import sessions
from clientapi.auth import AuthBearer


# Scenarios for sessions
# Scenario 01: no_auth
# Scenario 02: bearer
def test_sessions_no_auth():
    # When
    with sessions.no_auth() as s:
        # Then
        assert isinstance(s, Session)


def test_sessions_bearer():
    # Given
    token = "some_token"

    # When
    with sessions.bearer_auth(token) as s:
        # Then
        assert isinstance(s, Session)
        assert isinstance(s.auth, AuthBearer)

        dummy_request = DummyRequest()
        s.auth(dummy_request)
        assert dummy_request.headers["Authorization"] == f"Bearer {token}"


class DummyRequest:
    headers: dict = {}
