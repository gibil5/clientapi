from contextlib import contextmanager

from requests import Session

from clientapi.auth import AuthBearer


@contextmanager
def no_auth():
    """
    Creates a HTTP session with the default configuration
    Returns:
        Session
    """
    session = Session()
    yield session
    session.close()


@contextmanager
def bearer_auth(bearer_token):
    """
    Creates a HTTP session with a bearer token

    Args:
        bearer_token: token to use in the request

    Returns:
        Session
    """
    session = Session()
    session.auth = AuthBearer(bearer_token)
    yield session
    session.close()
