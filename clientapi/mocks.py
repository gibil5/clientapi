import functools
import json
import re
from http import HTTPStatus


def _strip_xml(xml):
    return re.sub(r"\s+", "", xml)


def _transform(body, headers):
    headers = headers or {}
    if body is not None:
        if isinstance(body, (dict, list)):
            body = json.dumps(body)
            headers["Content-Type"] = "application/json"
        elif isinstance(body, str):
            headers["Content-Type"] = "text/xml"
        else:
            raise ValueError(f"Not supported type for body: {type(body)}")
    else:
        body = ""
    return body, headers


def _get_request_body(request):
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        body = json.loads(request.body)
    elif content_type == "text/xml":
        body = _strip_xml(request.body)
    else:
        body = request.body
    return body


# pylint: disable=too-many-arguments
def http_callback(status_code, headers=None, body=None, request_body=None, request_headers=None, request_params=None):
    """
    Creates a callback for the responses library

    Args:
        status_code (HTTPStatus): status code to return in the callback
        headers (dict): headers to be returned in the response
        body (Any): body to be returned in the response
        request_body (Optional[Any]): expected body in the request
        request_headers (Optional[dict]): expected headers in the request
        request_params (Optional[dict]): expected query parameters in the request

    Returns:
        callable: function representing the callback
    """

    # Define values for response parameters
    body, headers = _transform(body, headers)

    # Define values for request parameters
    request_headers = request_headers or {}
    request_params = request_params or {}

    def request_callback(request):
        # Assert that the request header is the expected one
        for header, param_expected_value in request_headers.items():
            assert request.headers.get(header) == param_expected_value

        # Assert that the request body is the expected one
        if request_body:
            actual_body = _get_request_body(request)
            assert actual_body is not None, "Request body was not expected to be None"
            assert actual_body == request_body

        # Assert that the request params are the expected ones
        for param_name, param_expected_value in request_params.items():
            assert request.params.get(param_name) == param_expected_value

        return status_code, headers, body

    return request_callback


http_100_callback = functools.partial(http_callback, status_code=HTTPStatus.CONTINUE)
http_101_callback = functools.partial(http_callback, status_code=HTTPStatus.SWITCHING_PROTOCOLS)
http_102_callback = functools.partial(http_callback, status_code=HTTPStatus.PROCESSING)
http_200_callback = functools.partial(http_callback, status_code=HTTPStatus.OK)
http_201_callback = functools.partial(http_callback, status_code=HTTPStatus.CREATED)
http_202_callback = functools.partial(http_callback, status_code=HTTPStatus.ACCEPTED)
http_203_callback = functools.partial(http_callback, status_code=HTTPStatus.NON_AUTHORITATIVE_INFORMATION)
http_204_callback = functools.partial(http_callback, status_code=HTTPStatus.NO_CONTENT)
http_205_callback = functools.partial(http_callback, status_code=HTTPStatus.RESET_CONTENT)
http_206_callback = functools.partial(http_callback, status_code=HTTPStatus.PARTIAL_CONTENT)
http_207_callback = functools.partial(http_callback, status_code=HTTPStatus.MULTI_STATUS)
http_208_callback = functools.partial(http_callback, status_code=HTTPStatus.ALREADY_REPORTED)
http_226_callback = functools.partial(http_callback, status_code=HTTPStatus.IM_USED)
http_300_callback = functools.partial(http_callback, status_code=HTTPStatus.MULTIPLE_CHOICES)
http_301_callback = functools.partial(http_callback, status_code=HTTPStatus.MOVED_PERMANENTLY)
http_302_callback = functools.partial(http_callback, status_code=HTTPStatus.FOUND)
http_303_callback = functools.partial(http_callback, status_code=HTTPStatus.SEE_OTHER)
http_304_callback = functools.partial(http_callback, status_code=HTTPStatus.NOT_MODIFIED)
http_305_callback = functools.partial(http_callback, status_code=HTTPStatus.USE_PROXY)
http_307_callback = functools.partial(http_callback, status_code=HTTPStatus.TEMPORARY_REDIRECT)
http_308_callback = functools.partial(http_callback, status_code=HTTPStatus.PERMANENT_REDIRECT)
http_400_callback = functools.partial(http_callback, status_code=HTTPStatus.BAD_REQUEST)
http_401_callback = functools.partial(http_callback, status_code=HTTPStatus.UNAUTHORIZED)
http_402_callback = functools.partial(http_callback, status_code=HTTPStatus.PAYMENT_REQUIRED)
http_403_callback = functools.partial(http_callback, status_code=HTTPStatus.FORBIDDEN)
http_404_callback = functools.partial(http_callback, status_code=HTTPStatus.NOT_FOUND)
http_405_callback = functools.partial(http_callback, status_code=HTTPStatus.METHOD_NOT_ALLOWED)
http_406_callback = functools.partial(http_callback, status_code=HTTPStatus.NOT_ACCEPTABLE)
http_407_callback = functools.partial(http_callback, status_code=HTTPStatus.PROXY_AUTHENTICATION_REQUIRED)
http_408_callback = functools.partial(http_callback, status_code=HTTPStatus.REQUEST_TIMEOUT)
http_409_callback = functools.partial(http_callback, status_code=HTTPStatus.CONFLICT)
http_410_callback = functools.partial(http_callback, status_code=HTTPStatus.GONE)
http_411_callback = functools.partial(http_callback, status_code=HTTPStatus.LENGTH_REQUIRED)
http_412_callback = functools.partial(http_callback, status_code=HTTPStatus.PRECONDITION_FAILED)
http_413_callback = functools.partial(http_callback, status_code=HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
http_414_callback = functools.partial(http_callback, status_code=HTTPStatus.REQUEST_URI_TOO_LONG)
http_415_callback = functools.partial(http_callback, status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
http_416_callback = functools.partial(http_callback, status_code=HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
http_417_callback = functools.partial(http_callback, status_code=HTTPStatus.EXPECTATION_FAILED)
http_421_callback = functools.partial(http_callback, status_code=HTTPStatus.MISDIRECTED_REQUEST)
http_422_callback = functools.partial(http_callback, status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
http_423_callback = functools.partial(http_callback, status_code=HTTPStatus.LOCKED)
http_424_callback = functools.partial(http_callback, status_code=HTTPStatus.FAILED_DEPENDENCY)
http_426_callback = functools.partial(http_callback, status_code=HTTPStatus.UPGRADE_REQUIRED)
http_428_callback = functools.partial(http_callback, status_code=HTTPStatus.PRECONDITION_REQUIRED)
http_429_callback = functools.partial(http_callback, status_code=HTTPStatus.TOO_MANY_REQUESTS)
http_431_callback = functools.partial(http_callback, status_code=HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE)
http_500_callback = functools.partial(http_callback, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
http_501_callback = functools.partial(http_callback, status_code=HTTPStatus.NOT_IMPLEMENTED)
http_502_callback = functools.partial(http_callback, status_code=HTTPStatus.BAD_GATEWAY)
http_503_callback = functools.partial(http_callback, status_code=HTTPStatus.SERVICE_UNAVAILABLE)
http_504_callback = functools.partial(http_callback, status_code=HTTPStatus.GATEWAY_TIMEOUT)
http_505_callback = functools.partial(http_callback, status_code=HTTPStatus.HTTP_VERSION_NOT_SUPPORTED)
http_506_callback = functools.partial(http_callback, status_code=HTTPStatus.VARIANT_ALSO_NEGOTIATES)
http_507_callback = functools.partial(http_callback, status_code=HTTPStatus.INSUFFICIENT_STORAGE)
http_508_callback = functools.partial(http_callback, status_code=HTTPStatus.LOOP_DETECTED)
http_510_callback = functools.partial(http_callback, status_code=HTTPStatus.NOT_EXTENDED)
http_511_callback = functools.partial(http_callback, status_code=HTTPStatus.NETWORK_AUTHENTICATION_REQUIRED)
