from Libraries.Python.Command import Command
from Libraries.SimplePyGame.Positions import Vec2
from Libraries.SimplePyGame.SDL2.UI.Rectangle import Rectangle

from pygame._sdl2 import Renderer

from Libraries.SimplePyGame.UI.Mouse import Mouse


class Button(Rectangle):
    def __init__(self, pos: Vec2 | Vec2.NameSpaces.Value, size: Vec2 | Vec2.NameSpaces.Value, color,
                 render: Renderer | None = None, command: Command = None, disabled: bool = False):
        super().__init__(pos, size, color, render)
        self.Command = command
        self.is_disabled = disabled

    @property
    def is_enabled(self) -> bool:
        return not self.is_disabled



    def events(self):

        if not self.Command or self.is_disabled:
            return

        if self.hitbox.collidepoint(Mouse.pos().xy):
            self.Command()
