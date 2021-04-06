from contextlib import contextmanager

from requests import Session

from clientapi.auth import AuthBearer


@contextmanager
def plain():
    """
    Creates a HTTP session with the default configuration
    :returns: Session
    """
    session = Session()
    yield session
    session.close()


@contextmanager
def bearer(auth_token):
    """
    Creates a HTTP session with a bearer token
    :returns: Session
    """
    session = Session()
    session.auth = AuthBearer(auth_token)
    yield session
    session.close()
