from pygame._sdl2 import Texture, Renderer
from pygame import Rect

import Positions
from Libraries.SimplePyGame.Color import Color, NameSpaces as ColorNameSpaces
from Libraries.SimplePyGame.Positions import Vec2
from Libraries.SimplePyGame.SDL2.Text.DynamicText import DynamicText
from Libraries.SimplePyGame.SDL2.Text.FontInfo import FontInfo

from core.App import AppConfigs as App


class Text:

    def __init__(self, render: Renderer, pos, value, font: FontInfo | dict | list,
                 color: Color | ColorNameSpaces.color, visible: bool = True):

        self._initialized = False

        pos = pos if isinstance(pos, (tuple, list)) else pos.xy

        self.texture: Texture
        self.rect: Rect = Rect(pos, (0, 0))
        self.render: Renderer = render

        self.font = font if isinstance(font, FontInfo) else (FontInfo.from_dict(font) if
                                                             isinstance(font, dict) else FontInfo.from_sequence(font))

        _color = color if isinstance(color, Color) else Color(color)
        self.old_color = _color
        self.color = _color
        self.value = value
        self.is_visible = visible

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
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        if isinstance(value, Color):
            self.__color = value
        else:
            self.__color = Color.parse(value)

        if getattr(self, '_initialized', False) and self.old_color != self.color:
            self.generate_texture()
            self.old_color = self.color

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
