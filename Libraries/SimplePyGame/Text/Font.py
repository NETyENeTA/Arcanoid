import pygame as pg
import os

class Font:
    def __init__(self, name: str, path: str, size: int):
        self.name = name  # Уникальное имя в системе (например, "MainBold")
        self.path = path  # Путь к папке (например, "assets/fonts/")
        self.filename = name # Имя файла (например, "arial.ttf")
        self.size = size

    @property
    def real_font(self):
        return pg.font.Font(self.full_path, self.size)

    @property
    def full_path(self):
        # Собираем путь правильно через os.path.join
        return os.path.join(self.path, self.filename)

    @property
    def name(self): return self.__Name
    @name.setter
    def name(self, value):
        if '/' in value or '\\' in value:
            raise NameError('Name cannot contain slashes')
        self.__Name = value

    @property
    def size(self): return self.__Size
    @size.setter
    def size(self, value):
        self.__Size = value if value > 0 else 1