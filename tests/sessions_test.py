from requests import Session

from clientapi import sessions
from clientapi.auth import AuthBearer


# Scenarios for sessions
# Scenario 01: plain
# Scenario 02: bearer
def test_sessions_plain():
    # When
    with sessions.plain() as s:
        # Then
        assert isinstance(s, Session)


def test_sessions_bearer():
    # Given
    auth_token = "some_token"

    # When
    with sessions.bearer(auth_token) as s:
        # Then
        assert isinstance(s, Session)
        assert isinstance(s.auth, AuthBearer)

        dummy_request = DummyRequest()
        s.auth(dummy_request)
        assert dummy_request.headers["Authorization"] == f"Bearer {auth_token}"


class DummyRequest:
    headers: dict = {}
