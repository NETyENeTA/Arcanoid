import pygame as pg


class CashedFonts:
    def __init__(self):
        # Ключ: (полный_путь, размер), Значение: объект pg.font.Font
        self.__cached = {}

    def get_font(self, path: str, size: int) -> pg.font.Font:
        key = (path, size)

        # Если такого шрифта с таким размером еще нет в памяти — грузим
        if key not in self.__cached:
            try:
                self.__cached[key] = pg.font.Font(path, size)
            except FileNotFoundError:
                print(f"Error: Font file not found at {path}")
                # Запоминаем, что тут ошибка, и даем дефолт
                self.__cached[key] = pg.font.Font(None, size)

        return self.__cached[key]

    def clear(self):
        self.__cached.clear()