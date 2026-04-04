from pygame._sdl2 import Texture, Renderer
from pygame import Rect

from Libraries.SimplePyGame.Color import Color, NameSpaces as ColorNameSpaces
from Libraries.SimplePyGame.Positions import Vec2
from Libraries.SimplePyGame.SDL2.Text.DynamicText import DynamicText

from core.App import AppConfigs as App


class Text(DynamicText):

    def __init__(self, render: Renderer, pos, value, font, color: Color | ColorNameSpaces.color, visible: bool = True):

        # del self.__pos #Not need, its get from rect (rectangle properties)

        self._initialized = False

        self.texture: Texture | None = None
        self.rect: Rect = Rect(pos.xy, (0, 0))
        self.render: Renderer = render

        super().__init__(pos, value, font, color, visible)

        self.generate_texture()
        self._initialized = True

    def generate_texture(self):
        self.texture = App.FontS.get_texture(self.value, self.name, self.size, self.color.rgba)
        self.rect.w, self.rect.h = self.texture.width, self.texture.height

    def draw(self):

        if not self.is_visible:
            return

        self.texture.draw(dstrect=self.rect)

    @property
    def pos(self):
        return Vec2(self.rect.topleft)

    @pos.setter
    def pos(self, value: Vec2):
        if isinstance(value, Vec2):
            self.rect.topleft = value.xy

        elif isinstance(value, tuple):
            self.rect.topleft = value


    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value
        if getattr(self, '_initialized', False):
            self.generate_texture()

    @property
    def name(self):
        return self.font.name

    @name.setter
    def name(self, name: str):
        self.font.name = name
        if getattr(self, '_initialized', False):
            self.generate_texture()

    @property
    def size(self):
        return self.font.size

    @size.setter
    def size(self, size: int):
        self.font.size = size
        if getattr(self, '_initialized', False):
            self.generate_texture()
