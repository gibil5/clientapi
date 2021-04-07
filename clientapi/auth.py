from requests.auth import AuthBase

from clientapi.exceptions import APIClientError


class BearerTokenNotValid(APIClientError):
    code = "bearer_token_not_valid"
    detail = "The specified bearer token is not valid"
    source = None


class AuthBearer(AuthBase):  # pylint: disable=too-few-public-methods

    def __init__(self, token):
        self.token = token
        if not token:
            raise BearerTokenNotValid("No token set to query the API")

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r
