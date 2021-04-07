from pydantic import BaseModel

from clientapi import responses

# Scenarios for responses
# Scenario 01: entity
# Scenario 02: collection


def test_entity():
    obj = {"data": {"some_attr": "some_value"}}

    # When
    model = responses.entity(MyDummyModel)
    parsed = model.parse_obj(obj)

    # Then
    assert parsed.data.some_attr == "some_value"


def test_collection():
    obj = {"data": [{"some_attr": "some_value"}]}

    # When
    model = responses.collection(MyDummyModel)
    parsed = model.parse_obj(obj)

    # Then
    assert parsed.data[0].some_attr == "some_value"


class MyDummyModel(BaseModel):
    some_attr: str
