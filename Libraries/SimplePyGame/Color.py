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

    def __init__(self, red: int | NameSpaces.color = Default.RED,
                 green: int = Default.GREEN,
                 blue: int = Default.BLUE,
                 alpha: int = Default.ALPHA):


        if isinstance(red, (list, tuple, dict, str)):
            self.parse(red, instance=self)
            return

        self.r, self.g, self.b, self.a = red, green, blue, alpha

    @classmethod
    def parse(cls, value, instance=None):
        # Если на входе список или кортеж
        if isinstance(value, (list, tuple)):
            r, g, b = value[0], value[1], value[2]
            a = value[3] if len(value) > 3 else cls.Default.ALPHA
            return cls._setup(r, g, b, a, instance)

        # Если на входе словарь
        if isinstance(value, dict):
            r = value.get('r', value.get('red', cls.Default.RED))
            g = value.get('g', value.get('green', cls.Default.GREEN))
            b = value.get('b', value.get('blue', cls.Default.BLUE))
            a = value.get('a', value.get('alpha', cls.Default.ALPHA))
            return cls._setup(r, g, b, a, instance)

        # Если на входе строка (HEX или CSV)
        if isinstance(value, str):
            temp = cls.from_hex(value) if value.startswith('#') else cls.from_string(value)
            return cls._setup(temp.r, temp.g, temp.b, temp.a, instance)

        # Если ничего не подошло (fallback)
        return instance if instance else cls()

    @classmethod
    def _setup(cls, r, g, b, a, instance=None):
        """Вспомогательный метод, чтобы не дублировать логику применения значений"""
        if instance:
            instance.r, instance.g, instance.b, instance.a = r, g, b, a
            return instance
        return cls(r, g, b, a)


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
