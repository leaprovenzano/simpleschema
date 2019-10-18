import string
import re

import pytest


from hypothesis import strategies as st
from hypothesis import given, example

from simpleschema.constraints import InvalidConstraintError
from simpleschema.constraints import (
    MinLength,
    MaxLength,
    MinItems,
    MaxItems,
    Pattern,
    Minimum,
    Maximum,
    ExclusiveMaximum,
    ExclusiveMinimum,
    MultipleOf,
)


class ConstraintSuite:

    Constr = NotImplemented
    constr = NotImplemented

    def test_init_with_valid_constr(self, param):
        constr = self.Constr(param)
        assert constr.value == param

    def test_init_with_invalid_constr(self, param):
        with pytest.raises(InvalidConstraintError):
            self.Constr(param)

    def test_validate_on_valid(self, inp):
        assert self.constr(inp) is True

    def test_validate_on_invalid(self, inp):
        assert self.constr(inp) is False


class LengthConstraintSuite(ConstraintSuite):

    @given(st.integers(0))
    def test_init_with_valid_constr(self, param):
        super().test_init_with_valid_constr(param)

    @given(st.integers(max_value=-1) | st.floats() | st.text())
    def test_init_with_invalid_constr(self, param):
        super().test_init_with_invalid_constr(param)


class TestMinLength(LengthConstraintSuite):

    Constr = MinLength
    constr = MinLength(5)

    @given(st.text(min_size=5))
    def test_validate_on_valid(self, inp):
        super().test_validate_on_valid(inp)

    @given(st.text(max_size=4))
    def test_validate_on_invalid(self, inp):
        super().test_validate_on_invalid(inp)


class TestMaxLength(LengthConstraintSuite):

    Constr = MaxLength
    constr = MaxLength(5)

    @given(st.text(max_size=5))
    def test_validate_on_valid(self, inp):
        super().test_validate_on_valid(inp)

    @given(st.text(min_size=6))
    def test_validate_on_invalid(self, inp):
        super().test_validate_on_invalid(inp)


class TestMinItems(LengthConstraintSuite):

    Constr = MinItems
    constr = MinItems(5)

    @given(st.lists(st.integers() | st.text() | st.booleans(), min_size=5))
    def test_validate_on_valid(self, inp):
        super().test_validate_on_valid(inp)

    @given(st.lists((st.integers() | st.text() | st.booleans()), max_size=4))
    def test_validate_on_invalid(self, inp):
        super().test_validate_on_invalid(inp)


class TestMaxItems(LengthConstraintSuite):

    Constr = MaxItems
    constr = MaxItems(5)

    @given(st.lists((st.integers() | st.text() | st.booleans()), max_size=5))
    def test_validate_on_valid(self, inp):
        super().test_validate_on_valid(inp)

    @given(st.lists((st.integers() | st.text() | st.booleans()), min_size=6))
    def test_validate_on_invalid(self, inp):
        super().test_validate_on_invalid(inp)


class TestPattern(ConstraintSuite):

    Constr = Pattern
    constr = Pattern(r'^[a-z]+$')

    def test_init_with_valid_constr(self):
        inst = self.Constr(r'^boop$')
        assert isinstance(inst.expr, re.Pattern)

    @given(st.integers() | st.floats() | st.lists(st.text()))
    def test_init_with_invalid_constr(self, param):
        super().test_init_with_invalid_constr(param)

    @given(st.text(string.ascii_lowercase, min_size=1))
    def test_validate_on_valid(self, inp):
        super().test_validate_on_valid(inp)

    @example('boop1')
    @example('1boop')
    @given(st.text(string.digits + string.whitespace + string.ascii_uppercase))
    def test_validate_on_invalid(self, inp):
        super().test_validate_on_invalid(inp)


class NumericConstraintSuite(ConstraintSuite):

    @given(st.integers() | st.floats(allow_nan=False, allow_infinity=False))
    def test_init_with_valid_constr(self, param):
        super().test_init_with_valid_constr(param)

    @given(st.text(st.characters()) | st.none())
    def test_init_with_invalid_constr(self, param):
        super().test_init_with_invalid_constr(param)


class TestMinimum(NumericConstraintSuite):

    Constr = Minimum
    constr = Minimum(5)

    @given(st.integers(5) | st.floats(5.0, allow_nan=False, allow_infinity=False))
    def test_validate_on_valid(self, inp):
        super().test_validate_on_valid(inp)

    @given(
        st.integers(max_value=4) | st.floats(max_value=4.999, allow_nan=False, allow_infinity=False)
    )
    def test_validate_on_invalid(self, inp):
        super().test_validate_on_invalid(inp)


class TestMaximum(NumericConstraintSuite):

    Constr = Maximum
    constr = Maximum(5)

    @given(
        st.integers(max_value=5) | st.floats(max_value=5.0, allow_nan=False, allow_infinity=False)
    )
    def test_validate_on_valid(self, inp):
        super().test_validate_on_valid(inp)

    @given(
        st.integers(min_value=6)
        | st.floats(min_value=5.0001, allow_nan=False, allow_infinity=False)
    )
    def test_validate_on_invalid(self, inp):
        super().test_validate_on_invalid(inp)


class TestExclusiveMinimum(NumericConstraintSuite):

    Constr = ExclusiveMinimum
    constr = ExclusiveMinimum(5)

    @given(st.integers(6) | st.floats(6.99, allow_nan=False, allow_infinity=False))
    def test_validate_on_valid(self, inp):
        super().test_validate_on_valid(inp)

    @given(st.integers(max_value=5) | st.floats(max_value=5, allow_nan=False, allow_infinity=False))
    def test_validate_on_invalid(self, inp):
        super().test_validate_on_invalid(inp)


class TestExclusiveMaximum(NumericConstraintSuite):

    Constr = ExclusiveMaximum
    constr = ExclusiveMaximum(5)

    @given(
        st.integers(max_value=4) | st.floats(max_value=4.99, allow_nan=False, allow_infinity=False)
    )
    def test_validate_on_valid(self, inp):
        super().test_validate_on_valid(inp)

    @given(
        st.integers(min_value=5) | st.floats(min_value=5.0, allow_nan=False, allow_infinity=False)
    )
    def test_validate_on_invalid(self, inp):
        super().test_validate_on_invalid(inp)


class TestMultipleOf(ConstraintSuite):

    Constr = MultipleOf
    constr = MultipleOf(2)

    @given(st.integers(1))
    def test_init_with_valid_constr(self, param):
        super().test_init_with_valid_constr(param)

    @given(st.integers(max_value=0) | st.floats(max_value=0) | st.text())
    def test_init_with_invalid_constr(self, param):
        super().test_init_with_invalid_constr(param)

    @given(
        st.integers().filter(lambda x: x != 0).map(lambda x: x * 2)
        | st.integers().filter(lambda x: x != 0).map(lambda x: x * 2).map(float)
    )
    @example(2.0)
    @example(22)
    @example(4)
    def test_validate_on_valid(self, inp):
        super().test_validate_on_valid(inp)

    @given(
        st.integers().filter(lambda x: x % 2 != 0)
        | st.floats(allow_nan=False, allow_infinity=False).filter(lambda x: x % 2 != 0)
    )
    def test_validate_on_invalid(self, inp):
        super().test_validate_on_invalid(inp)
