import json
import time
from enum import Enum

import requests
from requests import HTTPError, Response

from clientapi.exceptions import APIHTTPError
from clientapi.logger import clientapi_logger


class ContentType(str, Enum):
    JSON = "application/json"
    XML = "text/xml"


def _create_headers(headers, data, content_type):
    headers = headers or {}

    if data and content_type:
        headers.update({"Content-Type": content_type})

    return headers


class ClientAPI:  # pylint: disable=too-few-public-methods
    """Base class to define thin clients to API Clients.

    Usage:
    >>> from clientapi import ClientAPI, parse
    >>>
    >>> class YourAPI(ClientAPI):
    >>>
    >>>     # This is totally optional
    >>>     def __init__(self, session, url="some default url"):
    >>>         super().__init__(session, url)
    >>>
    >>>
    >>>    def update_something(self, thing_id, payload: PayloadPydanticModel) -> SomethingPydanticModel:
    >>>         path = f"/something/{thing_id}"
    >>>         response = self.execute_request(
    >>>             path,
    >>>             method="PATCH",
    >>>             data=payload.json(),
    >>>         )
    >>>         return parse(response, model=SomethingPydanticModel)

    """

    def __init__(self, session, url, logger=None):
        """Instantiates a thin client to communicate with an API.

        Args:
            session (requests.Session): A initialized session instance.
            url (str): Base URL of the API.
            logger (Logger): Logger to use for debugging purposes. Defaults to lib logger
        """
        self._session = session
        self._url = url
        self._logger = logger or clientapi_logger

    def execute_request(
        self,
        resource,
        method="GET",
        params=None,
        headers=None,
        data=None,
        timeout=None,
        content_type: ContentType = ContentType.JSON,
    ) -> Response:  # pylint: disable=too-many-arguments
        """Low-level function for API calls.
        It wraps the requests library for managing sessions and custom Exceptions

        Args:
            resource (str): Path of the resource.
            method (str, optional): HTTP method to execute. Defaults to "GET".
            params (Dict[str, str], optional): Query parameters to include in the URL. Defaults to None.
            headers (Dict[str, str], optional): HTTP method to execute. Defaults to None.
            data (Any, optional): Payload to send in the body. Defaults to None.
            timeout (int, optional): Amount of seconds to wait for a timeout and raise an exception
            content_type (ContentType, optional): Content-type of data. Only used if data is present. Defaults to JSON.
        Raises:
            APIHTTPError: Error that occurred during the execution of the request if HTTPError takes place.

        Returns:
            Response: Model for the HTTP response in requests
        """
        url = f"{self._url}{resource}"
        try:
            headers = _create_headers(headers, data, content_type)

            self._logger.debug(f"Request: %s", _get_request_log_detail(url, method, headers, data, params))
            start = time.time()
            response = self._session.request(
                url=url,
                method=method,
                params=params,
                headers=headers,
                data=data,
                timeout=timeout,
            )
            end = time.time()
            self._logger.debug(f"Response: %s", _get_response_log_detail(response, start, end))
            response.raise_for_status()
            return response
        except HTTPError as err:
            raise APIHTTPError.wrap(err) from err


def _get_request_log_detail(url, method, headers, data, params):
    log_fields = {
        "url": url,
        "method": method,
    }

    if headers:
        log_fields["headers"] = headers
    if data:
        log_fields["data"] = data
    if params:
        log_fields["params"] = params

    return json.dumps(log_fields)


def _get_response_log_detail(response: requests.Response, start, end):
    log_fields = {
        "status_code": response.status_code,
        "time_ms": _get_elapsed_time_ms(start, end),
    }

    if response.text:
        log_fields["body"] = response.text
    if response.headers:
        log_fields["headers"] = dict(response.headers)

    return json.dumps(log_fields)


def _get_elapsed_time_ms(start, end):
    elapsed_seconds = end - start
    elapsed_ms = elapsed_seconds * 1000
    return round(elapsed_ms, 2)
