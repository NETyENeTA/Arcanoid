from Libraries.Math.Random import randrange_int as rnd
from Libraries.SimplePyGame.Color import Color, NameSpaces
from Libraries.SimplePyGame.Colors import Colors
from core.App import AppConfigs as App
from core.GameElements.Rectangle import Rectangle, pg
from Libraries.SimplePyGame.Positions import Range
from core.GameElements.ShadowCaster import ShadowCaster

from Libraries.Python.List import get_at


class Block(Rectangle, ShadowCaster):


    def __init__(self, pos, size, color: Color | NameSpaces.color | None = None, screen: pg.Surface = None,
                 *colors):
        Rectangle.__init__(self, pos, size, color if color else Colors.BLACK
                           , screen if screen else App.Screen.render)


        self.DefaultColor = self.color if color else None

        self.colors = colors

        self.minimalHealth = 0
        self.health = rnd(1, 3)
        self.shadow_info = Range(2, 0.1, 30)

        self.init_shadow()


    def draw_shadow_shape(self, surf, color):
        # Рисуем прямоугольник во весь размер поверхности
        pg.draw.rect(surf, color, (0, 0, *self.hitbox.size), border_radius=4)

    @property
    def is_dead(self) -> bool:
        return self.health == self.minimalHealth

    @property
    def is_alive(self) -> bool:
        return not self.is_dead

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        self.__health = value

        if not self.DefaultColor:
            self.color = get_at(self.colors, self.health - 1, self.DefaultColor)

        if self.health < self.minimalHealth:
            self.__health = self.minimalHealth

    @property
    def hp(self):
        return self.health

    @hp.setter
    def hp(self, value):
        self.health = value




