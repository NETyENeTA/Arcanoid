from Libraries.SimplePyGame.Color import Color
from Libraries.SimplePyGame.Positions import Vec2

from pygame import Rect


class Light:

    def __init__(self, pos: Vec2, color: Color, render):
        self.__pos: Vec2 = pos
        self.color = color

        self.render = render

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, pos: Vec2 | tuple[int, int] | tuple[float, float] | list[float] | list[int]) -> None:

        # todo self.pos = list => Vec2, not list
        if isinstance(pos, (tuple, list)):
            self.__pos.x = pos[0]
            self.__pos.y = pos[1]
        else:
            self.__pos = pos

    def draw(self):

        self.render.draw_color = self.color.rgb
        self.render.fill_rect(Rect(self.pos.xy, (10, 10)))
        self.render.draw_rect(Rect((self.pos - Vec2(5)).xy, (20, 20)))
