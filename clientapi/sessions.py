from contextlib import contextmanager

from requests import Session
from requests.auth import AuthBase, HTTPBasicAuth

from clientapi.auth import Bearer, SharedSecret


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
def bearer(bearer_token):
    """
    Creates a HTTP session with a bearer token

    Args:
        bearer_token: token to use as a bearer

    Returns:
        Session
    """
    session = Session()
    session.auth = Bearer(bearer_token)
    yield session
    session.close()


@contextmanager
def shared_secret(secret_key):
    """
    Creates a HTTP session with shared secret auth
    Args:
        secret_key (str): shared secret key value

    Returns:
        Session
    """
    session = Session()
    session.auth = SharedSecret(secret_key)
    yield session
    session.close()


@contextmanager
def basic(username, password):
    """
    Creates a HTTP session with basic auth
    Args:
        username (str): username to use in the session
        password (str): password to use in the session

    Returns:
        Session
    """
    session = Session()
    session.auth = HTTPBasicAuth(username, password)
    yield session
    session.close()


@contextmanager
def base(base_auth: AuthBase):
    """
    Creates a HTTP session using a AuthBase object
    Args:
        base_auth (AuthBase): AuthBase

    Returns:
        Session
    """
    session = Session()
    session.auth = base_auth
    yield session
    session.close()
