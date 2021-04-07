import json
from unittest.mock import Mock

import pytest
from pydantic import BaseModel

from clientapi import APIValidationError, parse

# Scenarios for parse
# Scenario 01: Success
# Scenario 02: Validation Error


def test_parse_success():
    # Given
    body = {"attribute": 1234}

    content = json.dumps(body).encode()

    response = Mock()
    response.content = content

    # When
    obj = parse(response, DummyModel)

    # Then
    return obj.attribute == body["attribute"]


def test_parse_validation_error():
    # Given
    body = {"not_the": "schema"}

    content = json.dumps(body).encode()

    response = Mock()
    response.content = content

    # When/Then
    with pytest.raises(APIValidationError):
        _ = parse(response, DummyModel)


class DummyModel(BaseModel):
    attribute: int
