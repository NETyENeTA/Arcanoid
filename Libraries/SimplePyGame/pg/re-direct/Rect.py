import pygame as pg

from Libraries.SimplePyGame.Positions import Vec2
from Libraries.SimplePyGame.Color import Color


class Rect:

    def __init__(self, screen,
                 pos: Vec2 | Vec2.NameSpaces.Value, size: Vec2 | Vec2.NameSpaces.Value,
                 color: Color | tuple[int, int, int] | tuple[int, int, int, int] | list[int] | dict = None):

        self.screen = screen

        self.pos = pos if isinstance(pos, Vec2) else Vec2(value=pos)
        self.size = size if isinstance(size, Vec2) else Vec2(value=size)

        if isinstance(color, (list, tuple)):
            color = Color(*color)

        elif isinstance(color, dict):
            color = Color(**color)

        self.color = color

    @property
    def hitbox(self):
        return self.pos.xy, self.size.xy

    @property
    def rect(self):
        return pg.Rect(self.hitbox)

    @rect.setter
    def rect(self, value: pg.Rect):
        self.pos.xy, self.size.xy = value

    @property
    def left(self):
        return self.pos.x

    @left.setter
    def left(self, value: int | float):
        self.pos.x = value

    @property
    def right(self):
        return self.pos.x + self.size.x

    @right.setter
    def right(self, value: float | int):
        self.pos.x = value - self.size.x

    @property
    def top(self):
        return self.pos.y

    @top.setter
    def top(self, value: float | int):
        self.pos.y = value

    @property
    def bottom(self):
        return self.pos.y + self.size.y

    @bottom.setter
    def bottom(self, value: float | int):
        self.pos.y = value - self.size.y

    @property
    def topleft(self):
        return self.pos + self.size // 2

    def draw(self):
        pg.draw.rect(self.screen, self.color.get_colorful(), self.hitbox)
