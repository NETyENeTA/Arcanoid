import os

class Font:
    def __init__(self, name: str, path: str, size: int, filename: str = None):
        self.name = name
        self.path = path
        self.filename = filename if filename else f"{name}.ttf"
        self.size = size

    @property
    def full_path(self):
        return os.path.join(self.path, self.filename)

    @property
    def name(self):
        return self.__Name
    @name.setter
    def name(self, value):
        if '/' in value or '\\' in value:
            raise NameError('Name cannot contain slashes')
        self.__Name = value
