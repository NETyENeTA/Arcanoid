from pygame._sdl2 import Texture
from pygame import Rect, Surface, SRCALPHA, transform, BLEND_ALPHA_SDL2

from Libraries.SimplePyGame.Positions import Vec2


import pygame as pg

class Gradient:

    class Modes:
        Horizontal = 0
        Vertical = 1

    def __init__(self, renderer, rect: Rect | tuple, mode: Modes | int, *colors):
        self.renderer = renderer

        # Храним Rect как область отрисовки
        self._rect = rect if isinstance(rect, Rect) else Rect(rect)

        if mode == Gradient.Modes.Horizontal:
            temp_surf = Surface((len(colors), 1), SRCALPHA)
            for i, color in enumerate(colors):
                temp_surf.set_at((i, 0), color.rgba)

        elif mode == Gradient.Modes.Vertical:
            temp_surf = Surface((1, len(colors)), SRCALPHA)
            for i, color in enumerate(colors):
                temp_surf.set_at((0, i), color.rgba)

        else:
            raise TypeError('Invalid mode')

        temp_surf = transform.smoothscale(temp_surf, self._rect.size)

        self._texture = Texture.from_surface(renderer, temp_surf)


    @property
    def pos(self) -> Vec2:
        # Возвращаем текущую позицию из нашего Rect
        return Vec2(self._rect.topleft)

    @pos.setter
    def pos(self, value):
        # Обновляем позицию Rect, чтобы blit знал, куда рисовать
        self._rect.topleft = value

    @property
    def texture(self) -> Texture:
        # Аналог property surface, теперь отдаем текстуру
        return self._texture

    @property
    def rect(self) -> Rect:
        # Возвращаем Rect, который описывает положение и размер на экране
        return self._rect

    def blit(self):
        # Используем внутренний rect для отрисовки
        self.renderer.blit(self._texture, self._rect)
