import random

from typing import TypeVar, List, Tuple
T = TypeVar('T')


def randrange_int(minimal: int, maximal: int) -> int:
    return random.randint(minimal, maximal)


def random_from_list(*values: List[T] | Tuple[T]) -> T:
    return random.choice(values)