from abc import ABCMeta, abstractmethod


class SchemaABC(metaclass=ABCMeta):

    type: str
    title: str
    description: str

    @abstractmethod
    def to_dict(self):
        return NotImplemented
