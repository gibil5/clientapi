from requests.auth import AuthBase

from clientapi.exceptions import APIClientError


class InvalidTokenError(APIClientError):
    code = "jwt_token_not_found"
    detail = "The requested token is not valid"
    source = None


class AuthBearer(AuthBase):  # pylint: disable=too-few-public-methods

    def __init__(self, token):
        self.token = token
        if not token:
            raise InvalidTokenError("No token set to query API-devices")

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r
