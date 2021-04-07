import json
from http import HTTPStatus
from uuid import UUID

import pytest
from pydantic import BaseModel, ValidationError
from requests import HTTPError, Request, Response

from clientapi import APIClientError, APIHTTPError, APIValidationError


# APIClientError Scenarios
# Scenario 01: Content
def test_api_client_error_content():
    # Given
    code = "validation_error"
    detail = "One or more parameters are invalid."
    source = [
        {
            "loc": ["query_parameters", "customer_id"],
            "msg": "value is not a valid uuid",
            "type": "type_error.uuid"
        }
    ]

    # When
    err = APIClientError(code, detail, source)
    content = err.content

    # Then
    assert content["code"] == code
    assert content["detail"] == detail
    assert content["source"] == source


# APIHTTPError Scenarios
# Scenario 01: HTTPError wrap
# Scenario 02: HTTPError with non-electric format
def test_http_error_wrap():
    # Given
    status_code = HTTPStatus.BAD_REQUEST
    code = "validation_error"
    detail = "One or more parameters are invalid."
    source = [
        {
            "loc": ["query_parameters", "customer_id"],
            "msg": "value is not a valid uuid",
            "type": "type_error.uuid"
        }
    ]

    error = {
        "code": code,
        "detail": detail,
        "source": source,
    }

    content = json.dumps(error).encode()

    url = "some_url"
    method = "GET"

    response = Response()
    response.status_code = status_code
    response._content = content
    response.url = url

    request = Request()
    request.method = method

    err = HTTPError()
    err.request = request
    err.response = response

    # When
    api_http_error = APIHTTPError.wrap(err)

    # Then
    assert api_http_error.code == "validation_error"
    assert api_http_error.detail == "One or more parameters are invalid."
    assert api_http_error.status_code == HTTPStatus.BAD_REQUEST
    assert api_http_error.source == source


def test_http_error_wrap_with_no_electric_format():
    # Given
    method = "GET"
    url = "some_url"
    status_code = HTTPStatus.CONFLICT

    response = Response()
    response.status_code = status_code
    response._content = b''
    response.url = url

    request = Request()
    request.method = method

    msg = "The message"
    err = HTTPError(msg)
    err.request = request
    err.response = response

    # When
    api_http_error = APIHTTPError.wrap(err)

    # Then
    assert api_http_error.code == "unknown"
    assert api_http_error.status_code == HTTPStatus.CONFLICT
    assert api_http_error.detail == msg

    expected_source = {
        "method": method,
        "url": url,
        "status_code": status_code,
        "text": "",
    }
    assert api_http_error.source == expected_source


# APIValidationError
# Scenario 01: ValidationError wrap
# Scenario 02: ValidationError wrap with Attribute Error
def test_validation_error_wrap():
    # Given
    messages = [{"loc": ("customer_id",), "msg": "field required", "type": "value_error.missing"}]

    with pytest.raises(ValidationError) as err_info:
        SomePydanticModel.parse_obj({})

    # When
    err = err_info.value
    electric_error = APIValidationError.wrap(err)

    # Then
    assert electric_error.code == "api_validation_error"
    assert electric_error.detail == "One or more parameters are invalid."
    assert electric_error.source == messages


def test_validation_error_attribute_error_wrap():
    # Given
    err = FakeValidationError()

    # When
    electric_error = APIValidationError.wrap(err)

    # Then
    assert electric_error.code == "api_validation_error"
    assert electric_error.detail == "One or more parameters are invalid."
    assert electric_error.source is None


class FakeValidationError(ValidationError):

    def __init__(self) -> None:
        super().__init__(None, None)

    def errors(self):
        raise AttributeError("Why? No hay why.")


class SomePydanticModel(BaseModel):
    customer_id: UUID
