import pygame as pg

from Libraries.SimplePyGame.Color import Color
from Libraries.SimplePyGame.Positions import Vec2


def draw_gradient(surface, color1, color2, rect):
    # Создаем временную поверхность 1x2 (для вертикального градиента)
    grad = pg.Surface((1, 2))
    grad.set_at((0, 0), color1)
    grad.set_at((0, 1), color2)

    # Растягиваем её до нужного размера сглаженным методом
    grad = pg.transform.smoothscale(grad, (rect.width, rect.height))
    surface.blit(grad, rect)

class Gradient:
    class Modes:
        Horizontal = 0
        Vertical = 1

    def __init__(self, rect: pg.Rect, mode: Modes | int, surface: pg.Surface | None = None, *colors: Color):
        self.mode = mode

        self._surface = surface
        self._pos = Vec2(rect.topleft)

        self.__surface: pg.Surface

        if mode == Gradient.Modes.Vertical:

            self.__surface = pg.Surface((1, len(colors)), pg.SRCALPHA)

            for i, color in enumerate(colors):
                self.__surface.set_at((0, i), color.rgba)

        elif mode == Gradient.Modes.Horizontal:
            self.__surface = pg.Surface((len(colors), 1), pg.SRCALPHA)

            for i, color in enumerate(colors):
                self.__surface.set_at((i, 0), color.rgba)

        self.__surface = pg.transform.smoothscale(self.__surface, rect.size)

    def blit(self):
        self._surface.blit(self.__surface, self.pos.xy)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos

    @property
    def surface(self) -> pg.Surface:
        return self.__surface

    @property
    def rect(self) -> pg.Rect:
        return self.__surface.get_rect()



