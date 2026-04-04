import os

from Libraries.SimplePyGame.SDL2.Text.FontInfo import FontInfo


class Font(FontInfo):
    def __init__(self, name: str, path: str, size: int, filename: str = None):
        super().__init__(name, size)

        self.path = path
        self.filename = self.filename if self.filename else (filename if filename else f"{name}.ttf")

    @property
    def full_path(self):
        return os.path.join(self.path, self.filename)


