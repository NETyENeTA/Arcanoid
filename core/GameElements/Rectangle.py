import pygame as pg

from Libraries.SimplePyGame.Positions import Vec2
from Libraries.SimplePyGame.Color import Color, NameSpaces
from Libraries.SimplePyGame.Screen import Screen

from core.App import AppConfigs as App

from pygame._sdl2.video import Renderer

from Libraries.SimplePyGame.SDL2.Draw import draw_circular_dashed_rect as draw_circular


class Rectangle:

    def __init__(self,
                 pos: Vec2 | Vec2.NameSpaces.Value, size: Vec2 | Vec2.NameSpaces.Value,
                 color: Color | NameSpaces.color = None,
                 render: Screen | None = None):

        render = render.render if isinstance(render, Screen) else render
        self.render : Renderer = render if render is None else App.Screen.render

        pos = pos if isinstance(pos, Vec2) else Vec2(value=pos)
        size = size if isinstance(size, Vec2) else Vec2(value=size)

        self.hitbox = pg.Rect(pos.xy, size.xy)

        if isinstance(color, (list, tuple)):
            color = Color(*color)

        elif isinstance(color, dict):
            color = Color(**color)

        self.color = color

    @property
    def center(self) -> Vec2:
        return Vec2(self.hitbox.center)

    # @property
    # def distance_to(self, pos: Vec2) -> float:
    #     ret

    @property
    def pos(self):
        return Vec2(self.hitbox.topleft)

    @pos.setter
    def pos(self, pos: Vec2):
        self.hitbox.topleft = pos.xy

    def draw(self):
        self.render.draw_color = self.color.rgba
        self.render.fill_rect(self.hitbox)