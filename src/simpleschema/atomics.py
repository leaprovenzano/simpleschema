from abc import abstractclassmethod, ABCMeta

from simpleschema.schema import BooleanSchema, IntegerSchema, NumberSchema, NullSchema, StringSchema


class SchemaType(metaclass=ABCMeta):

    __schema_cls__ = NotImplemented

    @abstractclassmethod
    def __schema__(cls, **kwargs):
        return NotImplemented

    def __subclasshook__(cls, t: type) -> bool:
        if cls is SchemaType:
            return hasattr(t.__schema__) and callable(t.__schema__)
        return NotImplemented


class AtomicSchema(SchemaType):

    __schema_cls__ = NotImplemented
    __atomic__ = True

    @abstractclassmethod
    def __schema__(cls, **kwargs):
        return cls.__schema_cls__(**kwargs).to_dict()


class String(SchemaType, str):

    __schema_cls__ = StringSchema


class Number(SchemaType, float):

    __schema_cls__ = NumberSchema


class Integer(SchemaType, int):

    __schema_cls__ = IntegerSchema


class Boolean(SchemaType):

    __supertype__ = bool
    __schema_cls__ = BooleanSchema

    def __new__(cls, x):
        return bool(x)


class Null(SchemaType):

    __supertype__ = type(None)
    _schema_cls = NullSchema

    def __new__(cls):
        return None
