import json
import logging
import re
from http import HTTPStatus
from logging import DEBUG, INFO

import pytest
import responses
from requests import Session

from clientapi import APIHTTPError, ClientAPI
from clientapi.mocks import http_200_callback, http_404_callback

log_regex = re.compile(r"(Response|Request): (.*)")


# ClientAPI Scenarios
# Scenario 01: Success - Execute with default logger enabled
# Scenario 02: Success - Execute with default logger disabled
# Scenario 03: Success - Execute with external logger
# Scenario 04: Failed - Execute HTTP Error
@responses.activate
def test_execute_success_with_default_logger_disabled(caplog):
    # Given
    url = "https://url.com"
    resource = "/hello"
    body = {"attribute": 1234}

    responses.add_callback(
        url=f"{url}{resource}",
        method="GET",
        callback=http_200_callback(body=body),
    )

    clientapi_logger = logging.getLogger("clientapi")
    clientapi_logger.setLevel(INFO)

    session = Session()

    # When
    api = ClientAPI(url=url, session=session)
    response = api.execute_request(resource=resource)

    # Then
    assert json.loads(response.content) == body
    assert len(caplog.records) == 0


@responses.activate
def test_execute_success_with_default_logger_enabled(caplog):
    # Given
    method = "POST"
    base_url = "https://url.com"
    resource = "/hello"
    body = {"attribute": 1234}
    request_body = {"attr": "abc"}
    request_params = {"page": "1"}

    url = f"{base_url}{resource}"
    responses.add_callback(
        url=url,
        method=method,
        callback=http_200_callback(
            body=body,
            request_body=request_body,
            request_params=request_params,
        ),
    )

    clientapi_logger = logging.getLogger("clientapi")
    clientapi_logger.setLevel(DEBUG)

    session = Session()

    # When
    api = ClientAPI(url=base_url, session=session)
    response = api.execute_request(
        method="POST",
        resource=resource,
        data=json.dumps(request_body),
        params=request_params,
    )

    # Then
    assert json.loads(response.content) == body
    assert len(caplog.records) == 2

    # Assert request log
    request_log = caplog.records[0]
    assert request_log.levelname == "DEBUG"

    request_log_groups = log_regex.search(request_log.message)
    assert request_log_groups[1] == "Request"

    request_log_groups = log_regex.search(request_log.message)
    request_log_detail = json.loads(request_log_groups[2])
    assert request_log_detail["url"] == url
    assert request_log_detail["method"] == method
    assert request_log_detail["headers"] == {"Content-Type": "application/json"}
    assert request_log_detail["data"] == json.dumps(request_body)
    assert request_log_detail["params"] == request_params

    # Assert response log
    response_log = caplog.records[1]
    assert response_log.levelname == "DEBUG"

    response_log_groups = log_regex.search(response_log.message)
    assert response_log_groups[1] == "Response"

    response_log_groups = log_regex.search(response_log.message)
    response_log_detail = json.loads(response_log_groups[2])
    assert response_log_detail["status_code"] == HTTPStatus.OK
    assert isinstance(response_log_detail["time_ms"], float)
    assert response_log_detail["body"] == json.dumps(body)
    assert response_log_detail["headers"] == {"Content-Type": "application/json"}


@responses.activate
def test_execute_success_with_default_external_logger(caplog):
    # Given
    method = "GET"
    base_url = "https://url.com"
    resource = "/hello"
    body = {"attribute": 1234}

    url = f"{base_url}{resource}"
    responses.add_callback(
        url=url,
        method=method,
        callback=http_200_callback(body=body),
    )

    test_logger = logging.getLogger("test_logger")
    test_logger.setLevel(DEBUG)

    session = Session()

    # When
    api = ClientAPI(url=base_url, session=session, logger=test_logger)
    response = api.execute_request(resource=resource)

    # Then
    assert json.loads(response.content) == body
    assert len(caplog.records) == 2

    # Assert request log
    request_log = caplog.records[0]
    assert request_log.levelname == "DEBUG"

    request_log_groups = log_regex.search(request_log.message)
    assert request_log_groups[1] == "Request"

    request_log_groups = log_regex.search(request_log.message)
    request_log_detail = json.loads(request_log_groups[2])
    assert request_log_detail["url"] == url
    assert request_log_detail["method"] == method

    # Assert response log
    response_log = caplog.records[1]
    assert response_log.levelname == "DEBUG"

    response_log_groups = log_regex.search(response_log.message)
    assert response_log_groups[1] == "Response"

    response_log_groups = log_regex.search(response_log.message)
    response_log_detail = json.loads(response_log_groups[2])
    assert response_log_detail["status_code"] == HTTPStatus.OK
    assert isinstance(response_log_detail["time_ms"], float)
    assert response_log_detail["body"] == json.dumps(body)
    assert response_log_detail["headers"] == {"Content-Type": "application/json"}


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
