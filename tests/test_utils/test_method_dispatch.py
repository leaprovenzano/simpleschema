import pytest
from simpleschema.utils import method_dispatch


def test_method_dispatch():
    class ThisError(Exception):

        pass

    class SomeClass:

        @method_dispatch
        def addone(self, i):
            raise ThisError('i must be an int')

        @addone.register
        def _(self, i: int) -> int:
            return i + 1

    inst = SomeClass()
    assert inst.addone(1) == 2
    with pytest.raises(ThisError):
        inst.addone('boop')
