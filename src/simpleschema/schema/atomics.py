from typing import Union, ClassVar, get_type_hints

from simpleschema.formats import Format
from simpleschema.utils import to_pascalcase
from simpleschema.types import JSONABLE
from simpleschema.schema.base import SchemaABC


class AtomicSchema(SchemaABC):

    def __init_subclass__(cls, **kwargs):
        cls._fields = get_type_hints(cls)
        cls._aliases = {k: to_pascalcase(k) for k in cls._fields}
        super().__init_subclass__(**kwargs)

    def __init__(self, **kwargs):
        self.__dict__['_fields_set'] = ['type']
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __setattr__(self, k: str, v: JSONABLE):
        if k not in self._fields:
            raise ValueError(f'field {k} is invalid for {self.__class__.__name__}')

        if k in self._fields_set:
            raise ValueError(f'fields in a schema are immutable once set')

        self.__dict__[k] = v
        self._fields_set.append(k)

    def to_dict(self):
        return {self._aliases.get(k, k): getattr(self, k) for k in self._fields_set}


class StringSchema(AtomicSchema):

    type: ClassVar[str] = 'string'
    min_length: int
    max_length: int
    pattern: str
    format: Format

    def __getattribute__(self, k: str):
        if k == 'format':
            return self.__dict__[k].value
        return super().__getattribute__(k)


class BaseNumericSchema(AtomicSchema):

    minimum: Union[int, float]
    maximum: Union[int, float]
    exclusive_minimum: Union[int, float]
    exclusive_maximum: Union[int, float]
    multiple_of: Union[int, float]


class NumberSchema(BaseNumericSchema):

    type: ClassVar[str] = 'number'


class IntegerSchema(BaseNumericSchema):

    type: ClassVar[str] = 'integer'


class NullSchema(AtomicSchema):

    type: ClassVar[str] = 'null'


class BooleanSchema(AtomicSchema):

    type: ClassVar[str] = 'boolean'
