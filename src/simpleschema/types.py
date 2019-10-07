from typing import Dict, Union, List
from abc import abstractclassmethod, ABCMeta


JSONABLE = Union[bool, type(None), str, int, float, List['JSONABLE'], Dict[str, 'JSONABLE']]


class SchemaType(metaclass=ABCMeta):

    __schema_cls__ = NotImplemented

    @abstractclassmethod
    def __schema__(cls, **kwargs):
        return NotImplemented

    def __subclasshook__(cls, t: type) -> bool:
        if cls is SchemaType:
            return hasattr(t.__schema__) and callable(t.__schema__)
        return NotImplemented
