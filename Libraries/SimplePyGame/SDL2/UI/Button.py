from Event.CommandStuff.Command import Command
from Libraries.SimplePyGame.Positions import Vec2
from Libraries.SimplePyGame.SDL2.UI.ButtonColors import ButtonColors
from Libraries.SimplePyGame.SDL2.UI.Rectangle import Rectangle

from pygame._sdl2 import Renderer

from Libraries.SimplePyGame.UI.Mouse import Mouse


class Button(Rectangle):
    def __init__(self, pos: Vec2 | Vec2.NameSpaces.Value, size: Vec2 | Vec2.NameSpaces.Value,
                 color: ButtonColors,
                 render: Renderer | None = None, command: Command = None, disabled: bool = False):
        super().__init__(pos, size, None, render)
        self.Command = command
        self.is_disabled = disabled
        self.color = color
        self.is_pressed = False

    @property
    def is_enabled(self) -> bool:
        return not self.is_disabled

    @property
    def is_hovered(self) -> bool:
        return self.hitbox.collidepoint(Mouse.pos().xy)

    def switch(self, disabled: bool | None = None):

        if disabled is not None:
            self.is_disabled = disabled
            return

        self.is_disabled = not self.is_disabled

    def press(self):

        if not self.Command or self.is_disabled:
            self.is_pressed = self.is_enabled
            return

        self.is_pressed = self.is_hovered

    def invoke(self):
        if self.is_pressed and self.is_hovered:
            self.Command()
        self.is_pressed = False

    def draw(self):

        if self.is_pressed:
            self.render.draw_color = self.color.pressed.rgba

        elif self.is_disabled:
            self.render.draw_color = self.color.disabled.rgba

        elif self.is_hovered:
            self.render.draw_color = self.color.hover.rgba

        else:
            self.render.draw_color = self.color.default.rgba

        self.render.fill_rect(self.hitbox)
