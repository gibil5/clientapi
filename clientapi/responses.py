from typing import Any, List, Optional, Type

import pydantic
from pydantic import BaseModel


class JsonAPIErrorResponse(BaseModel):
    """
    Schema to model a JsonAPI styled response

    It only models a subset of the recommended attributes. Also, is good to consider
    that this schema is used as a top level one, not wrapped up in `errors` as the spec
    recommends.

        "Error objects MUST be returned as an array keyed by errors in the top level of a JSON:API document"

    Future version of this library will try to include that, but so far in this current version
    there is no need to support that.

    Docs:
    https://jsonapi.org/format/#error-objects
    """
    code: str
    detail: str
    source: Optional[Any]


class ElectricAPIResponse(BaseModel):
    data: Any


def entity(model: Type[BaseModel]) -> Type[ElectricAPIResponse]:
    attrs = {"data": (model, None)}
    return pydantic.create_model(
        "ElectricAPIEntityResponse",
        __base__=ElectricAPIResponse,
        **attrs,
    )


def collection(model: Type[BaseModel]) -> Type[ElectricAPIResponse]:
    attrs = {"data": (List[model], None)}
    return pydantic.create_model(
        "ElectricAPICollectionResponse",
        __base__=ElectricAPIResponse,
        **attrs,
    )
