from typing import Type

from pydantic import BaseModel, ValidationError
from requests import Response

from clientapi.exceptions import APIValidationError


def parse(response: Response, model: Type[BaseModel]):
    """
    Parses a responses content to a pydantic model
    Args:
        response: requests library model for HTTP response
        model: pydantic model for parsing the response
    Raises:
        APIHTTPError: When a pydantic validation error occurs
    Returns:
        Instance of the specified model
    """
    try:
        return model.parse_raw(response.content)
    except ValidationError as err:
        raise APIValidationError.wrap(err)
