from typing import Set
from functools import lru_cache
from abc import abstractclassmethod, ABCMeta

from simpleschema.utils import to_pascalcase


@lru_cache(maxsize=32)
def pascalize(s: str):
    return to_pascalcase(s)


class SchemaType(metaclass=ABCMeta):

    __schema_type__: str = NotImplemented
    __valid_constraints__: Set[str] = set([])
    __valid_descriptors__: Set[str] = {'title', 'description'}

    @classmethod
    def _extract_descriptors(cls, **kwargs):
        return {pascalize(k): v for k, v in kwargs.items() if k in cls.__valid_descriptors__}

    @classmethod
    def _extract_constraints(cls, **kwargs):
        return {pascalize(k): v for k, v in kwargs.items() if k in cls.__valid_constraints__}

    @abstractclassmethod
    def schema(cls, **kwargs):
        schema = {
            'type': cls.__schema_type__,
            **cls._extract_descriptors(**kwargs),
            **cls._extract_constraints(**kwargs),
        }
        return schema


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

    @classmethod
    def __new__(cls, x):
        return bool(x)


class Null(SchemaType):

    __supertype__ = type(None)
    __schema_type__ = 'null'

    def __new__(cls):
        return None
