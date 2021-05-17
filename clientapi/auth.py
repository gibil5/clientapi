from requests.auth import AuthBase

from clientapi.exceptions import APIClientError


class InvalidBearerToken(APIClientError):
    code = "invalid_bearer_token"
    detail = "The specified bearer token is not valid"
    source = None


class InvalidSharedSecretKey(APIClientError):
    code = "invalid_shared_secret_key"
    detail = "The secret key is not valid"
    source = None


class Bearer(AuthBase):  # pylint: disable=too-few-public-methods

    def __init__(self, token):
        self.token = token
        if not token:
            raise InvalidBearerToken("No token set to query the API")

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r


class SharedSecret(AuthBase):  # pylint: disable=too-few-public-methods

    def __init__(self, key):
        if not key:
            raise InvalidSharedSecretKey("No secret key found")

        self.key = key

    def __call__(self, r):
        r.headers["SHARED_SECRET"] = self.key
        return r
