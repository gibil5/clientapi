from typing import Any, List, Optional, Type

import pydantic
from pydantic import BaseModel


class JsonAPIErrorResponse(BaseModel):
    """
    Schema to model a JsonAPI error response

    It only models a subset of the recommended attributes. Also, have in mind
    that this schema is used as a top level one, not wrapped up in `errors` as the spec
    recommends.

        "Error objects MUST be returned as an array keyed by errors in the top level of a JSON:API document"

    Future version of this library will try to include that, but so far in this current version
    there is no need to support it.

    Docs:
    https://jsonapi.org/format/#error-objects
    """
    code: str
    detail: str
    source: Optional[Any]


class JsonAPIResponse(BaseModel):
    """
    Schema to model a JsonAPI styled primary data response

    Docs:
    https://jsonapi.org/format/#document-top-level
    """
    data: Any


def entity(model: Type[BaseModel]) -> Type[JsonAPIResponse]:
    """
    Wraps a model in the JsonAPIResponse format for an entity
    Args:
        model: pydantic model to wrap

    Returns:
        JsonAPIResponse

    """
    attrs = {"data": (model, None)}
    return pydantic.create_model(
        "JsonAPIEntityResponse",
        __base__=JsonAPIResponse,
        **attrs,
    )


def collection(model: Type[BaseModel]) -> Type[JsonAPIResponse]:
    """
    Wraps a model in the JsonAPIResponse format for a collection
    Args:
        model: pydantic model to wrap

    Returns:
        JsonAPIResponse

    """
    attrs = {"data": (List[model], None)}
    return pydantic.create_model(
        "JsonAPICollectionResponse",
        __base__=JsonAPIResponse,
        **attrs,
    )
