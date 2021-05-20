import json
from http import HTTPStatus

import pytest
import responses
from requests import Session

from clientapi import APIHTTPError, ClientAPI
from clientapi.mocks import http_200_callback, http_404_callback


# ClientAPI Scenarios
# Scenario 01: Execute Success
# Scenario 02: Execute HTTP Error
@responses.activate
def test_execute_success():
    # Given
    url = "https://url.com"
    resource = "/hello"
    body = {"attribute": 1234}

    responses.add_callback(
        url=f"{url}{resource}",
        method="GET",
        callback=http_200_callback(body=body),
    )

    session = Session()

    # When
    api = ClientAPI(url=url, session=session)
    response = api.execute_request(resource=resource)

    # Then
    assert json.loads(response.content) == body


@responses.activate
def test_execute_http_error():
    # Given
    url = "https://url.com"
    resource = "/hello"
    method = "GET"
    body = {"error": "not_found"}

    responses.add_callback(
        url=f"{url}{resource}",
        method=method,
        callback=http_404_callback(body=body),
    )

    session = Session()

    # When
    api = ClientAPI(url=url, session=session)

    with pytest.raises(APIHTTPError) as ex_info:
        api.execute_request(resource=resource)

    err = ex_info.value
    assert err.code == "unknown"
    assert err.status_code == HTTPStatus.NOT_FOUND
    assert err.detail == "HTTPStatus.NOT_FOUND Client Error: Not Found for url: https://url.com/hello"

    expected_source = {
        "method": method,
        "status_code": HTTPStatus.NOT_FOUND,
        "text": json.dumps(body),
        "url": f"{url}{resource}",
    }
    assert err.source == expected_source
