from symtable import Class

class NameSpaces:

    color_rgb = tuple[int, int, int]  | list[int] | dict
    color_rgba = tuple[int, int, int, int] | list[int] | dict
    color = tuple[int, int, int, int] | tuple[int, int, int]  | list[int] | dict


class Color:
    class Default:
        RED = 255
        GREEN = 255
        BLUE = 255
        ALPHA = 255

    def __init__(self, red: int = Default.RED,
                 green: int = Default.GREEN,
                 blue: int = Default.BLUE,
                 alpha: int = Default.ALPHA):
        self.r = red
        self.g = green
        self.b = blue
        self.a = alpha


    @staticmethod
    def _clamp(value):
        return max(0, min(255, int(value)))

    @classmethod
    def mono_color(cls, value: int):
        return cls(value, value, value)

    @classmethod
    def mono_color_with_alpha(cls, value: int, alpha: int):
        return cls(value, value, value, alpha)

    @classmethod
    def mono_color_alpha(cls, value: int):
        return cls(value, value, value, value)

    @property
    def r(self):
        return self.__r
    @r.setter
    def r(self, value):
        self.__r = self._clamp(value)

    @property
    def g(self):
        return self.__g
    @g.setter
    def g(self, value):
        self.__g = self._clamp(value)

    @property
    def b(self):
        return self.__b
    @b.setter
    def b(self, value):
        self.__b = self._clamp(value)

    @property
    def a(self):
        return self.__a
    @a.setter
    def a(self, value):
        self.__a = self._clamp(value)

    def to_hex(self, include_alpha=False):
        if include_alpha:
            # :02x означает: 16-ричный формат, 2 символа, дополнить нулем
            return f"#{self.r:02x}{self.g:02x}{self.b:02x}{self.a:02x}".upper()

        return f"#{self.r:02x}{self.g:02x}{self.b:02x}".upper()

    @property
    def hex(self):
        return self.to_hex()

    @property
    def hexa(self):
        return self.to_hex(include_alpha=True)

    @classmethod
    def from_hex(cls, hex_str):
        hex_str = hex_str.lstrip('#')
        components = [int(hex_str[i:i + 2], 16) for i in range(0, len(hex_str), 2)]
        return cls(*components)

    @classmethod
    def from_string(cls, color_str: str):
        components = [int(x.strip()) for x in color_str.split(',')]

        return cls(*components)

    @property
    def rgb(self):
        return self.r, self.g, self.b

    @property
    def rgba(self):
        return self.r, self.g, self.b, self.a

    def __iter__(self):
        return iter(self.rgba)

    @property
    def full(self):
        return self.rgba

    def __repr__(self):
        return f"Color(r={self.r}, g={self.g}, b={self.b}, a={self.a})"

    def __str__(self):
        return f"{self.r}, {self.g}, {self.b}, {self.a}"
