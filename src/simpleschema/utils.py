"""generic utilities used by the simpleschema lib.
"""


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
