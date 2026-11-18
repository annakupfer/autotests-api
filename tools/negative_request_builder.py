from typing import TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def build_negative_request(
        request: T,
        field: str,
        value: object
) -> T:
    request_data = request.model_dump()
    request_data[field] = value

    return type(request).model_construct(**request_data)

