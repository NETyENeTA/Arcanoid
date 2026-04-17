from collections.abc import Callable

from Colors import Colors
from Event.CommandStuff.Command import Command
from Libraries.Animations.Functions.Lerp import lerp
from Positions import Vec2
from Text.Text import Text
from UI.InteractiveButton import InteractiveButton
from UI.Surface import Surface

from core.App import AppConfigs as App, WindowConfig as WC, pg

from pygame._sdl2 import Renderer

from core.GameElements.Paddle import Paddle


class PauseMenu:
    class Default:
        PADDLE_BOUNCE = 50
        BG_COLOR = Colors.GRAY
        SELECT = 1

    class Targets:

        DISABLED = (WC.Center[0], WC.H_Hidden)
        ENABLED = WC.Surface

    def __init__(self, paddle: Paddle, restart: Callable, render: Renderer = None):
        surface = Surface((400, 30), (0, 0), render)
        self.target = surface.rect.center = PauseMenu.Targets.DISABLED

        self.surface = surface
        self.render = surface.render
        self.active = False

        # self.texts = [
        #     Text(self.render, (0, 0), "Restart", ("koulen", 25), Colors.BLACK),
        #     Text(self.render, (0, 0), "Resume", ("koulen", 25), Colors.BLACK),
        #     Text(self.render, (0, 0), "Options", ("koulen", 25), Colors.BLACK),
        #     Text(self.render, (0, 0), "Settings", ("koulen", 25), Colors.BLACK),
        # ]

        self.InteractiveBtns = [
            InteractiveButton(Vec2.Zero,
                              Text(self.render, Vec2.Zero, "Restart", ("koulen", 25), Colors.BLACK),
                              Command(restart)),
            InteractiveButton(Vec2.Zero,
                              Text(self.render, Vec2.Zero, "Resume", ("koulen", 25), Colors.BLACK),
                              Command(self.resume)),
            InteractiveButton(Vec2.Zero,
                              Text(self.render, Vec2.Zero, "Options", ("koulen", 25), Colors.BLACK),
                              Command(None), disabled=True),
            InteractiveButton(Vec2.Zero,
                              Text(self.render, Vec2.Zero, "Exit", ("koulen", 25), Colors.BLACK),
                              Command(App.stop)),
        ]

        # center = (Vec2(self.surface.rect.center) - self.surface.rect.topleft)
        center = Vec2(50, self.surface.rect.centery - self.surface.rect.top)
        self.InteractiveBtns[0].text.rect.center = center.xy
        center = (center + Vec2(100,0))
        self.InteractiveBtns[1].text.rect.center = center.xy
        center = (center + Vec2(100, 0))
        self.InteractiveBtns[2].text.rect.center = center.xy
        self.InteractiveBtns[3].text.rect.center = (center + Vec2(80,0)).xy

        self.currentChoice = -1
        self.select = PauseMenu.Default.SELECT

        self.paddle = paddle


        self.PaddleYTargets = {
            "default": paddle.pos.y,
            "upper": paddle.pos.y - PauseMenu.Default.PADDLE_BOUNCE,
        }

    def toggle_pause(self, need_pause: bool = True):
        if need_pause:
            App.toggle_pause()
        self.toggle_active()

    def resume(self):
        App.Runtime.IsPause = False
        # self.active = False
        # self.toggle_active()
        self.switch_active(False)

    @property
    def select(self):
        return self.currentChoice


    @select.setter
    def select(self, value):

        if value == self.select or not self.InteractiveBtns:
            return

        if value < 0:
            value = len(self.InteractiveBtns) - 1
        elif value >= len(self.InteractiveBtns):
            value = 0

        # self.InteractiveBtns[self.select].text.color = Colors.BLACK
        # self.currentChoice = value
        # self.InteractiveBtns[self.select].text.color = Colors.WHITE

        btn = self.InteractiveBtns[self.select]
        btn.text.color = Colors.BLACK_RED if btn.disabled else Colors.BLACK
        btn.selected = False

        self.currentChoice = value

        btn = self.InteractiveBtns[self.select]
        btn.text.color = Colors.RED if btn.disabled else Colors.WHITE
        btn.selected = True

    def check_buttons(self):
        for btn in self.InteractiveBtns:
            if btn.selected and not btn.disabled:
                btn.command()
                break

    @property
    def pos(self):
        return self.surface.rect.topleft

    @property
    def size(self):
        return self.surface.rect.size

    def switch_active(self, active: bool):

        if self.active == active:
            return

        self.toggle_active()

    def toggle_active(self):
        if self.active:
            self.select = PauseMenu.Default.SELECT
            self.paddle.target_y = self.PaddleYTargets["default"]
            self.target = PauseMenu.Targets.DISABLED
            self.active = False
        else:
            if self.pos[0] < self.paddle.pos.x + self.paddle.hitbox.size[0] and \
                    self.pos[0] + self.size[0] > self.paddle.pos.x:
                self.paddle.target_y = self.PaddleYTargets["upper"]
            self.target = PauseMenu.Targets.ENABLED
            self.active = True

    def update(self):
        self.surface.rect.y = lerp(self.surface.rect.y, self.target[1], 0.1)

    @property
    def overdrawn(self):
        return self.pos[1] >= WC.H

    def draw(self):

        if self.overdrawn:
            return

        with self.surface.capture():
            # self.render.draw_color = Colors.RED.rgb
            # self.render.fill_rect(pg.Rect(10, 10, 30, 30))

            for btn in self.InteractiveBtns:
                btn.draw()

        self.surface.draw()
        self.surface.clear(PauseMenu.Default.BG_COLOR.rgba)


def main():
    pass


if __name__ == "__main__":
    main()
