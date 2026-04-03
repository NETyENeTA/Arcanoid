from Libraries.SimplePyGame.Colors import Colors
from Libraries.SimplePyGame.UI.Mouse import Mouse, pg, Vec2


class Cursor:

    def __init__(self, render = None, color = Colors.BLACK, size: Vec2 = Vec2(10, 10)) -> None:

        self.render = render
        self.color = color
        self.size = size


    @property
    def pressed(self):
        return Mouse.pressed()

    @property
    def pressed_all_5(self):
        return Mouse.pressed(5)

    @property
    def right(self):
        return self.pressed[0]

    @property
    def middle(self):
        return self.pressed[1]

    @property
    def left(self):
        return self.pressed[2]

    @property
    def pos(self) -> Vec2:
        return Mouse.pos()

    @property
    def pos_tuple(self):
        return pg.mouse.get_pos()

    @pos.setter
    def pos(self, value: Vec2):
        pg.mouse.set_pos(value.xy)

    def draw(self):

        self.render.draw_color = self.color.rgb
        self.render.fill_rect(pg.Rect(self.pos_tuple, self.size.xy))

    def draw_center(self):
        self.render.draw_color = self.color.rgb
        self.render.fill_rect(pg.Rect((self.pos - self.size / 2).xy, self.size.xy))
