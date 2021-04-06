from http import HTTPStatus
from typing import Any

from pydantic import ValidationError
from requests import HTTPError

from clientapi.responses import ElectricAPIErrorResponse


class APIClientError(Exception):
    code: str = None
    detail: str = None
    source: Any = None

    def __init__(self, code=None, detail=None, source=None):
        if code:
            self.code = code

        if detail:
            self.detail = detail

        if source:
            self.source = source

        message = f"({self.code}) {self.detail}."

        if source:
            message += f"Source: {str(source)}"
            self.source = source

        super().__init__(message)

    @property
    def content(self):
        return {
            "code": self.code,
            "detail": self.detail,
            "source": self.source,
        }


class APIValidationError(APIClientError):
    code = "api_validation_error"
    detail = "One or more parameters are invalid."

    @classmethod
    def wrap(cls, error: ValidationError):

        try:
            source = error.errors()
        except AttributeError:
            source = None
        return cls(source=source)


class APIHTTPError(APIClientError):
    status_code: HTTPStatus = None

    def __init__(self, code, detail, source, status_code):
        if status_code:
            self.status_code = status_code

        super().__init__(code, detail, source)

    @classmethod
    def wrap(cls, http_error: HTTPError):

        try:
            error = ElectricAPIErrorResponse.parse_raw(http_error.response.content)
            code = error.code
            detail = error.detail
            source = error.source
        except ValidationError:
            code = "unknown"
            detail = str(http_error)
            source = {
                "method": getattr(http_error.request, "method", None),
                "url": getattr(http_error.response, "url", None),
                "status_code": getattr(http_error.response, "status_code", None),
                "text": getattr(http_error.response, "text", None),
            }

        status_code = http_error.response.status_code

        return cls(code=code, detail=detail, source=source, status_code=status_code)
