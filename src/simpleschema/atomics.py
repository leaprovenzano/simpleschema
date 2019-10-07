from simpleschema.schema import BooleanSchema, IntegerSchema, NumberSchema, NullSchema, StringSchema
from simpleschema.types import SchemaType


class AtomicSchema(SchemaType):

    __schema_cls__ = NotImplemented
    __atomic__ = True

    def __schema__(cls, **kwargs):
        return cls.__schema_cls__(**kwargs).to_dict()


class String(AtomicSchema, str):

    __schema_cls__ = StringSchema


class Number(AtomicSchema, float):

    __schema_cls__ = NumberSchema


class Integer(AtomicSchema, int):

    __schema_cls__ = IntegerSchema


class Boolean(AtomicSchema):

    __supertype__ = bool
    __schema_cls__ = BooleanSchema

    def __new__(cls, x):
        return bool(x)


class Null(AtomicSchema):

    __supertype__ = type(None)
    _schema_cls = NullSchema

    def __new__(cls):
        return None
