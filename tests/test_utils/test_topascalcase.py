import string
from hypothesis import given, example
from hypothesis import strategies as st

from simpleschema.utils import to_pascalcase


_words = st.lists(st.text(string.ascii_lowercase, min_size=1), min_size=1)


@st.composite
def pascal(draw):
    words = draw(st.shared(_words, key='k'))
    pascal = words[0]
    for w in words[1:]:
        pascal += f'{w[0].upper()}{w[1:]}'
    return pascal


@st.composite
def py_identifier(draw):
    return '_'.join(draw(st.shared(_words, key='k')))


@given(inp=py_identifier(), expected=pascal())
@example(inp='word', expected='word')
@example(inp='my_identifier', expected='myIdentifier')
@example(inp='my_long_identifier', expected='myLongIdentifier')
def test_to_pascalcase(inp: str, expected: str):
    result = to_pascalcase(inp)
    assert result == expected
