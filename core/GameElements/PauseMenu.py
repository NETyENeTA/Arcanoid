from Colors import Colors
from Libraries.Animations.Functions.Lerp import lerp
from Text.Text import Text
from UI.Surface import Surface

from core.App import AppConfigs as App, WindowConfig as WC, pg

from pygame._sdl2 import Renderer

from core.GameElements.Paddle import Paddle


class PauseMenu:
    class Default:
        PADDLE_BOUNCE = 40
        BG_COLOR = Colors.GRAY

    class Targets:

        DISABLED = (WC.Center[0], WC.H)
        ENABLED = WC.Surface

    def __init__(self, paddle: Paddle, render: Renderer = None):
        surface = Surface((400, 30), (0, 0), render)
        self.target = surface.rect.center = PauseMenu.Targets.DISABLED

        self.surface = surface
        self.render = surface.render
        self.active = False

        self.texts = [
            Text(self.render, (0, 0), "Resume", ("koulen", 25), Colors.BLACK),
        ]

        self.texts[0].rect.center = (self.surface.rect.center)

        self.paddle = paddle

    def toggle_active(self):
        if self.active:
            self.paddle.bounce(PauseMenu.Default.PADDLE_BOUNCE)
            self.target = PauseMenu.Targets.DISABLED
            self.active = False
        else:
            self.paddle.bounce(-PauseMenu.Default.PADDLE_BOUNCE)
            self.target = PauseMenu.Targets.ENABLED
            self.active = True

    def update(self):
        self.surface.rect.y = lerp(self.surface.rect.y, self.target[1], 0.1)

    def draw(self):
        with self.surface.capture():
            # self.render.draw_color = Colors.RED.rgb
            # self.render.fill_rect(pg.Rect(10, 10, 30, 30))

            for text in self.texts:
                text.draw()

        self.surface.draw()
        self.surface.clear(PauseMenu.Default.BG_COLOR.rgba)


def main():
    pass


if __name__ == "__main__":
    main()
