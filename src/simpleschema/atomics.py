from typing import Dict, Union, List, Set
from functools import lru_cache
from abc import abstractclassmethod, ABCMeta

from simpleschema.utils import to_pascalcase

JSONABLE = Union[bool, type(None), str, int, float, List['JSONABLE'], Dict[str, 'JSONABLE']]


@lru_cache(maxsize=32)
def pascalize(s: str):
    return to_pascalcase(s)


class SchemaDict(dict):

    def __set_item__(self, k: str, v: JSONABLE):
        if v is not None:
            super()[pascalize(k)] = v


class SchemaType(metaclass=ABCMeta):

    __schema_type__: str = NotImplemented
    __valid_constraints__: Set[str] = set([])
    __valid_descriptors__: Set[str] = {'title', 'description'}

    @classmethod
    def _valid_fields(cls):
        cls.__valid_descriptors__ | cls.__valid_constraints__

    @abstractclassmethod
    def schema(cls, **kwargs):
        schema = SchemaDict(type=cls.__schema_type__)
        valid_fields = cls.__valid_descriptors__ | cls.__valid_constraints__
        for k, v in kwargs.items():
            if k in valid_fields:
                schema[k] = v
            else:
                raise ValueError(f'{k} is not a valid field for schema type {cls.__schema_type__}')
        return schema

    def __subclasshook__(cls, t: type) -> bool:
        if cls is SchemaType:
            return hasattr(t.schema) and callable(t.schema)
        return NotImplemented


class String(SchemaType, str):

    __schema_type__ = 'string'
    __valid_constraints__ = {'min_length', 'max_length', 'format', 'pattern'}


class NumericSchema(SchemaType):

    __valid_constraints__ = {
        'minimum',
        'maximum',
        'exclusive_minimum',
        'exclusive_maximum',
        'multiple_of',
    }


class Number(NumericSchema, float):

    __schema_type__ = 'number'


class Integer(NumericSchema, int):

    __schema_type__ = 'integer'


class Boolean(SchemaType):

    __supertype__ = bool
    __schema_type__ = 'boolean'

    def __new__(cls, x):
        return bool(x)


class Null(SchemaType):

    __supertype__ = type(None)
    __schema_type__ = 'null'

    def __new__(cls):
        return None
