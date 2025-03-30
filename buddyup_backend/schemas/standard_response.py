from typing import Generic, TypeVar, Optional
from pydantic.generics import GenericModel

T = TypeVar("T")

class StandardResponse(GenericModel, Generic[T]):
    status: str
    message: str
    id: Optional[int] = None
    data: Optional[T] = None