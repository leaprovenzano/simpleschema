import re
import typing as t
from abc import ABCMeta, abstractmethod
from simpleschema.utils import to_pascalcase, method_dispatch


Numeric = t.NewType('Numeric', t.Union[int, float])


class InvalidConstraintError(ValueError):

    def __init__(self, name, msg):
        super().__init__(f'Invalid constraint {name} : {msg}')


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


class LengthConstraint(Constraint):

    value: int

    @method_dispatch
    def __init__(self, value):
        raise InvalidConstraintError(self.__pyname__, 'must an integer')

    @__init__.register
    def _(self, value: int):
        if value < 0:
            raise InvalidConstraintError(self.__pyname__, 'must be positive')
        self.value = value


class MinLength(LengthConstraint):

    __pyname__ = 'min_length'

    def __call__(self, x: t.Sized) -> bool:
        return len(x) >= self.value


class MaxLength(LengthConstraint):

    __pyname__ = 'max_length'

    def __call__(self, x: t.Sized) -> bool:
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
        except (re.error, TypeError) as err:
            raise InvalidConstraintError(self.__pyname__, f'Invalid pattern : {err}')

    def __call__(self, s: str) -> bool:
        return self.expr.match(s) is not None


class NumericConstraint(Constraint):

    @method_dispatch
    def __init__(self, value):
        raise InvalidConstraintError(self.__pyname__, 'must an numeric type')

    @__init__.register
    def _(self, value: float):
        self.value = value

    @__init__.register
    def _(self, value: int):
        self.value = value


class Minimum(NumericConstraint):

    __pyname__ = 'minimum'

    value: Numeric

    def __call__(self, x: Numeric) -> bool:
        return x >= self.value


class Maximum(NumericConstraint):

    __pyname__ = 'maximum'

    value: Numeric

    def __call__(self, x: Numeric) -> bool:
        return x <= self.value


class ExclusiveMinimum(NumericConstraint):

    __pyname__ = 'exclusive_minimum'

    value: Numeric

    def __call__(self, x: Numeric) -> bool:
        return x > self.value


class ExclusiveMaximum(NumericConstraint):

    __pyname__ = 'exclusive_maxiumum'

    value: Numeric

    def __call__(self, x: Numeric) -> bool:
        return x < self.value


class MultipleOf(NumericConstraint):

    __pyname__ = 'multiple_of'

    value: Numeric

    def _validate_value(self, value: Numeric) -> Numeric:
        if value > 0:
            return value
        raise InvalidConstraintError(self.__pyname__, 'must be > 0')

    @method_dispatch
    def __init__(self, value):
        raise InvalidConstraintError(self.__pyname__, 'must an numeric type')

    @__init__.register
    def _(self, value: float):
        self.value = self._validate_value(value)

    @__init__.register
    def _(self, value: int):
        self.value = self._validate_value(value)

    def __call__(self, x: Numeric) -> bool:
        return x % self.value == 0
