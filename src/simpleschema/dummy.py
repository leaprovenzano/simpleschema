from typing import List


some_dict = {'a': 1, 'b': [1, 2, 3], 'c': {'a': 1, 'b': 2}}


class SomeClass:

    classattr: int = 1

    def __init__(self, boop: str):
        self.boop = boop
        self.bop = f'{boop}-{self.classattr}'

    def somemeth(self, data: List[int]) -> List[int]:
        return data + [self.classattr]
