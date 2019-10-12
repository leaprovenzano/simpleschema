import re
import typing as t
from abc import ABCMeta, abstractmethod
from simpleschema.utils import to_pascalcase


Numeric = t.NewType('Numeric', t.Union[int, float])


def is_implemented(attr):
    return attr != NotImplemented


class Constraint(metaclass=ABCMeta):

    __pyname__ = NotImplemented
    __alias__ = NotImplemented

    def __init_subclass__(cls):
        if is_implemented(cls.__pyname__):
            cls.__alias__ = to_pascalcase(cls.__pyname__)
        super().__init_subclass__()

    @abstractmethod
    def __call__(self, x) -> bool:
        return NotImplemented


class InvalidConstraintError(ValueError):

    def __init__(self, name, msg):
        super().__init__(f'Invalid constraint {name} : {msg}')


class LengthConstraint(Constraint):

    value: int

    def __init__(self, value: int):
        try:
            value = int(value)
        except TypeError:
            raise InvalidConstraintError(self.__pyname__, 'must an integer')
        if value < 0:
            raise InvalidConstraintError(self.__pyname__, 'must be positive')
        self.value = value


class MinLength(LengthConstraint):

    __pyname__ = 'min_length'

    def __call__(self, x: t.Iterable) -> bool:
        return len(x) >= self.value


class MaxLength(Constraint):

    __pyname__ = 'max_length'

    def __call__(self, x: t.Iterable) -> bool:
        return len(x) <= self.value


class MinItems(MinLength):

    __pyname__ = 'min_items'


class MaxItems(MaxLength):

    __pyname__ = 'max_items'


class Pattern(Constraint):

    __pyname__ = 'pattern'

    value: str

    def __init__(self, value: str):
        try:
            self.expr = re.compile(value)
        except re.error as err:
            InvalidConstraintError(self.__pyname__, f'Invalid pattern : {err}')

    def __call__(self, s: str) -> bool:
        return self._exp.match(s) is not None


class Minimum(Constraint):

    __pyname__ = 'minimum'

    value: Numeric

    def __call__(self, x: Numeric) -> bool:
        return x >= self.value


class Maximum(Constraint):

    __pyname__ = 'maxiumum'

    value: Numeric

    def __call__(self, x: Numeric) -> bool:
        return x <= self.value


class ExclusiveMinimum(Constraint):

    __pyname__ = 'exclusive_minimum'

    value: Numeric

    def __call__(self, x: Numeric) -> bool:
        return x > self.value


class ExclusiveMaximum(Constraint):

    __pyname__ = 'exclusive_maxiumum'

    value: Numeric

    def __call__(self, x: Numeric) -> bool:
        return x < self.value


class MultipleOf(Constraint):

    __pyname__ = 'multiple_of'

    value: Numeric

    def __call__(self, x: Numeric) -> bool:
        return x % self.value == 0
