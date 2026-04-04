class FontInfo:

    def __init__(self, name: str, size: int | None=None):
        self.name = name
        self.size = size
        self.filename: str | None = name if ".ttf" in name else None

    @classmethod
    def from_sequence(cls, seq: tuple | list):
        return cls(name=seq[0], size=seq[1])


    @classmethod
    def from_dict(cls, kwargs:dict):
        return cls(name=kwargs["name"], size=kwargs["size"])


    @property
    def name(self):
        return self.__Name

    @name.setter
    def name(self, value):
        if '/' in value or '\\' in value:
            raise NameError('Name cannot contain slashes')
        self.__Name = value.replace('.ttf', '')
