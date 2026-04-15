import random

from typing import TypeVar, List, Tuple, Sequence

T = TypeVar('T')


def randrange_int(minimal: int, maximal: int) -> int:
    return random.randint(minimal, maximal)


def random_from_list(*values: List[T] | Tuple[T]) -> T:
    return random.choice(values)

def choice(*sequences: list[T] | tuple[T] | T) -> T:
    return random.choice(sequences)


def roll_true_bool(rate: int | float) -> bool:
    return random.random() <= rate

def roll_false_bool(rate: int | float) -> bool:
    return random.random() >= rate

def roll_boolean():
    return choice(True, False)

def roll_bool(*sequences: list[bool] | tuple[bool] | bool) -> bool:
    return choice(*sequences)

def shaffle(*sequence: Sequence[T]) -> T:
    shaffle(sequence)

def shaffled(sequence: Sequence[T]) -> T:
    result = list(sequence)
    shaffle(result)
    return result