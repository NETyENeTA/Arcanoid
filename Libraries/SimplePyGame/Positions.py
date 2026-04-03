from pygame.math import Vector2
from Libraries.SimplePyGame.Color import NameSpaces
from Libraries.Animations.Functions.Lerp import lerp


class Vec2:
    class NameSpaces:
        Value = tuple[int, int] | tuple[float, float] | list[float] | list[int] | dict

    def __init__(self, x: int | NameSpaces.Value | float = None,
                 y: int | float = None,
                 value: NameSpaces.Value | None = None):

        if isinstance(x, (int, float)) and y is None:
            x, y = x, x

        if isinstance(x, (list, tuple)):
            x, y = x

        elif value is not None:
            x, y = value

        self.x = x
        self.y = y

    def lerp(self, other: "Vec2", t: float) -> "Vec2":
        return Vec2(
            lerp(self.x, other[0], t),
            lerp(self.y, other[1], t)
        )

    def normalize(self) -> None:
        self.x, self.y = self.normalized

    def reflect_x(self, to_negative: bool):
        if to_negative:
            self.x = -abs(self.x)
        else:
            self.x = abs(self.x)

    def reflect_y(self, to_negative: bool):
        if to_negative:
            self.y = -abs(self.y)
        else:
            self.y = abs(self.y)

    @property
    def to_vector2(self) -> Vector2:
        return Vector2(self.__x, self.__y)

    @property
    def difference(self) -> int:
        return self.x - self.y

    @property
    def difference_reversed(self) -> int:
        return self.y - self.x

    @property
    def subtracted_x(self) -> "Vec2":
        return Vec2(self.difference, self.y)

    def subtracted_y(self) -> "Vec2":
        return Vec2(self.x, self.difference_reversed)

    def copy(self) -> "Vec2":
        return Vec2(self.x, self.y)

    @property
    def magnitude(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    @property
    def normalized(self) -> "Vec2":
        mgt = self.magnitude

        if mgt == 0:
            return Vec2(0, 0)
        return Vec2(self.x / mgt, self.y / mgt)

    def __neg__(self) -> "Vec2":
        return Vec2(-self.x, -self.y)

    def __getitem__(self, key: int | str) -> float:
        if key == 0 or key == "x":
            return self.x
        if key == 1 or key == "y":
            return self.y
        raise KeyError(f"Key {key} not found in Vec2")

    def __setitem__(self, key: int | str, value: float):
        if key == 0 or key == "x":
            self.x = value
        elif key == 1 or key == "y":
            self.y = value
        else:
            raise KeyError(f"Key {key} not found in Vec2")

    def __len__(self) -> int:
        return int(self.length)

    @property
    def length(self) -> int | float:
        return self.x ** 2 + self.y ** 2

    def __iter__(self):
        yield self.x
        yield self.y

    def __abs__(self):
        return Vec2(abs(self.x), abs(self.y))

    def __iadd__(self, other):
        if isinstance(other, Vec2):
            self.x += other.x
            self.y += other.y

        elif isinstance(other, (tuple, list)):
            self.x += other[0]
            self.y += other[1]

        elif isinstance(other, (int, float)):
            self.x += other
            self.y += other
        else:
            raise TypeError("Can only add Vec2, int or float")
        return self

    def __isub__(self, other):
        if isinstance(other, Vec2):
            self.x -= other.x
            self.y -= other.y

        elif isinstance(other, (tuple, list)):
            self.x -= other[0]
            self.y -= other[1]

        elif isinstance(other, (int, float)):
            self.x -= other
            self.y -= other
        else:
            raise TypeError("Can only subtract Vec2, int or float")
        return self

    def __imul__(self, other):
        if isinstance(other, Vec2):
            self.x *= other.x
            self.y *= other.y
        elif isinstance(other, (int, float)):
            self.x *= other
            self.y *= other
        else:
            raise TypeError("Can only multiply Vec2, int or float")
        return self

    def __itruediv__(self, other):
        if isinstance(other, Vec2):
            self.x /= other.x
            self.y /= other.y
        elif isinstance(other, (int, float)):
            self.x /= other
            self.y /= other
        else:
            raise TypeError("Can only divide Vec2, int or float")
        return self

    def __add__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)

        if isinstance(other, (tuple, list)):
            return Vec2(self.x + other[0], self.y + other[1])

        if isinstance(other, (int, float)):
            return Vec2(self.x + other, self.y + other)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x - other.x, self.y - other.y)

        if isinstance(other, (tuple, list)):
            return Vec2(self.x - other[0], self.y - other[1])

        if isinstance(other, (int, float)):
            return Vec2(self.x - other, self.y - other)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x * other.x, self.y * other.y)
        if isinstance(other, (int, float)):
            return Vec2(self.x * other, self.y * other)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x / other.x, self.y / other.y)
        if isinstance(other, (int, float)):
            return Vec2(self.x / other, self.y / other)
        return NotImplemented

    def __floordiv__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x // other.x, self.y // other.y)
        if isinstance(other, (int, float)):
            return Vec2(self.x // other, self.y // other)
        return NotImplemented

    def __mod__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x % other.x, self.y % other.y)
        if isinstance(other, (int, float)):
            return Vec2(self.x % other, self.y % other)
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Vec2):
            return self.x == other.x and self.y == other.y
        if isinstance(other, (int, float)):
            return self.x == other and self.y == other
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, Vec2):
            return self.x < other.x and self.y < other.y
        if isinstance(other, (int, float)):
            return self.x < other and self.y < other
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Vec2):
            return self.x <= other.x and self.y <= other.y
        if isinstance(other, (int, float)):
            return self.x <= other and self.y <= other
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Vec2):
            return self.x > other.x and self.y > other.y
        if isinstance(other, (int, float)):
            return self.x > other and self.y > other
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Vec2):
            return self.x >= other.x and self.y >= other.y
        if isinstance(other, (int, float)):
            return self.x >= other and self.y >= other
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    @staticmethod
    def set(value: NameSpaces.Value):

        if isinstance(value, dict):
            return Vec2(**value)

        return Vec2(*value)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    @property
    def xy(self):
        return self.__x, self.__y

    @xy.setter
    def xy(self, value: tuple[int, int] | tuple[float, float] | list[float] | list[int]):
        self.__x, self.__y = value

    def __repr__(self):
        return f"Vec2(x={self.x}, y={self.y})"

    def __str__(self):
        return f"Vec2({self.x}; {self.y})"


class Range:

    def __init__(self, maximal, middle, minimal):
        self.maximal = maximal
        self.middle = middle
        self.minimal = minimal


def main():
    a = Vec2(0.5, 1)
    print(a)
    a.reflect_x(True)
    print(a, "invert_x true")
    a.reflect_x(False)
    print(a, "invert_x false")
    print("-------------")
    a.reflect_x(True)
    a.reflect_x(True)
    print(a, "invert_x true")
    a.reflect_x(False)
    a.reflect_x(False)
    print(a, "invert_x false")


if __name__ == "__main__":
    main()
