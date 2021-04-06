from typing import Any, List, Optional, Type

import pydantic
from pydantic import BaseModel


class ElectricAPIErrorResponse(BaseModel):
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
