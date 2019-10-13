"""generic utilities used by the simpleschema lib.
"""
from typing import Callable
import functools


def to_pascalcase(s: str) -> str:
    """convert a python identifier string to pascal case.

    Examples:
        >>> to_pascalcase('my_identifier')
        myIdentifier
        >>> to_pascalcase('my_long_identifier')
        myLongIdentifier
        >>> to_pascalcase('crab')
        crab
    """
    first, *other = s.split('_')
    return f'{first}{"".join([word.title() for word in other])}'


def method_dispatch(f: Callable) -> Callable:
    """a single dispatch wrapper for methods. Inspects the first arguement *after* self.

    functools standard `singledispatch` decorator looks at the first arg, to find the type and so it
    obvi messes up when called with self.
    This functionality will be in the standard `functools.singledistpatch` in python 3.8.

    Args:
        f (Callable): method to decorate as single dispatch

    Returns:
        Callable: decorated method
    """
    dispatcher = functools.singledispatch(f)

    @functools.wraps(f)
    def wrapper(self, *args, **kw):
        return dispatcher.dispatch(args[0].__class__)(self, *args, **kw)

    wrapper.register = dispatcher.register
    return wrapper
