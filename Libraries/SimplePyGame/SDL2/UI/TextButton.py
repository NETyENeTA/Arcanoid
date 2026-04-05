from Libraries.SimplePyGame.Positions import Vec2
from Libraries.SimplePyGame.SDL2.Text.FontInfo import FontInfo
from Libraries.SimplePyGame.SDL2.Text.Text import Text
from Libraries.SimplePyGame.SDL2.UI.Button import Button, ButtonColors, Renderer, Command
from Libraries.SimplePyGame.SDL2.UI.TextButtonColors import TextButtonColors

from core.App import AppConfigs as App

class TextButton(Button):


    def __init__(self, pos, size, text, font: FontInfo, color: ButtonColors, color_text: TextButtonColors,
                 render: Renderer | None=None, command:Command | None = None,
                 disabled: bool = False):


        super().__init__(pos, size, color, render, command, disabled)

        self.textColor = color_text

        self.text = Text(self.render, pos, text, font, self.textColor.default)

    # @property
    # def center(self):
    #     return self.hitbox.center
    #
    # @center.setter
    # def center(self, value):
    #
    #     if isinstance(value, Vec2):
    #         self.hitbox.center = value.xy
    #
    #     elif isinstance(value, (list, tuple)):
    #         self.hitbox.center = value
    #
    #     elif isinstance(value, dict):
    #         self.hitbox.center = (value.get('x', 0), value.get('y', 0))
    #
    #     self.text.pos = self.hitbox.topleft
    #
    #
    # @property
    # def pos(self):
    #     return self.hitbox.topleft
    #
    #
    # @pos.setter
    # def pos(self, value):
    #     if isinstance(value, Vec2):
    #         self.hitbox.topleft = value.xy
    #
    #     elif isinstance(value, (list, tuple)):
    #         self.hitbox.topleft = value
    #
    #     elif isinstance(value, dict):
    #         self.hitbox.topleft = (value.get('x', 0), value.get('y', 0))
    #
    #     self.text.pos = self.hitbox.topleft



    def draw(self):

        self.text.rect.center = self.hitbox.center

        if self.is_pressed:
            self.render.draw_color = self.color.pressed.rgba
            self.text.color = self.textColor.pressed

        elif self.is_disabled:
            self.render.draw_color = self.color.disabled.rgba
            self.text.color = self.textColor.disabled

        elif self.is_hovered:
            self.render.draw_color = self.color.hover.rgba
            self.text.color = self.textColor.hover

        else:
            self.render.draw_color = self.color.default.rgba
            self.text.color = self.textColor.default

        self.render.fill_rect(self.hitbox)
        self.text.draw()
