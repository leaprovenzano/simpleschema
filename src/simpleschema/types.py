from typing import Dict, Union, List

JSONABLE = Union[bool, type(None), str, int, float, List['JSONABLE'], Dict[str, 'JSONABLE']]
