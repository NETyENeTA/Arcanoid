import pygame as pg
from pygame.math import Vector2

from Libraries.SimplePyGame.Positions import Vec2
from Libraries.SimplePyGame.Color import Color


class Rectangle:

    def __init__(self, screen,
                 pos: Vec2 | Vec2.NameSpaces.Value, size: Vec2 | Vec2.NameSpaces.Value,
                 color: Color | tuple[int, int, int] | tuple[int, int, int, int] | list[int] | dict = None):

        self.screen = screen

        pos = pos if isinstance(pos, Vec2) else Vec2(value=pos)
        size = size if isinstance(size, Vec2) else Vec2(value=size)

        self.hitbox = pg.Rect(pos.xy, size.xy)

        if isinstance(color, (list, tuple)):
            color = Color(*color)

        elif isinstance(color, dict):
            color = Color(**color)

        self.color = color

    @property
    def rect(self):
        return self.hitbox

    @rect.setter
    def rect(self, value):
        self.hitbox = value

    @property
    def vec(self):
        return Vector2(self.rect.x, self.rect.y)

    @vec.setter
    def vec(self, value: Vector2):
        self.hitbox.topleft = value.xy

    @property
    def vec2(self):
        return Vec2(self.rect.x, self.rect.y)

    @vec2.setter
    def vec2(self, value: Vec2):
        self.hitbox.topleft = value.xy


    @property
    def pos(self):
        return self.hitbox.topleft

    @pos.setter
    def pos(self, value):
        self.hitbox.topleft = value

    @property
    def size(self):
        return self.hitbox.size

    @size.setter
    def size(self, value):
        self.hitbox.size = value

    def draw(self):
        pg.draw.rect(self.screen, self.color.get_colorful(), self.hitbox)
