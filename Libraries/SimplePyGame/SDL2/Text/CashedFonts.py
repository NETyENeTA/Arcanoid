import pygame as pg

class CashedFonts:
    def __init__(self):
        self.__cached = {}

    def get_font(self, path: str, size: int) -> pg.font.Font:
        key = (path, size)
        if key not in self.__cached:
            print(f'Font {path} not found in CashedFonts.')
            try:
                print(f"Trying to load font and cash it '{path}'...")
                self.__cached[key] = pg.font.Font(path, size)
            except Exception:
                print(f"Font Cash System doesn't find an exist file in '{path}'.")
                self.__cached[key] = pg.font.Font(None, size)
        return self.__cached[key]

    def clear(self):
        self.__cached.clear()
