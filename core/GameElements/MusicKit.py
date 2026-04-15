from pygame._sdl2 import Renderer

from Colors import Colors, Color
from Event.CommandStuff.Command import Command
from Libraries.Animations.Functions.Lerp import lerp
from Positions import Vec2
from Text.Text import Text
from UI.Surface import Surface
from core.GameElements.Paddle import Paddle

from core.App import AppConfigs as App, WindowConfig as WC, pg
from core.GameElements.PauseMenu import PauseMenu


class MusicKit:

    class Default:
        BG_COLOR = Colors.GRAY
        FILLER_COLOR = Colors.GRAY + Color.mono_color(30)
        PADDLE_BOUNCE = 50
        FADEOUT = 0.015
        OFFSET_X = 60

    class Targets:
        HIDDEN = (WC.MusicKit[0], WC.H)
        ACTIVE = WC.MusicKit

    def __init__(self, paddle: Paddle, pause_menu: PauseMenu, render: Renderer = None):
        surface = Surface((300, 30), (0, 0), render)

        self.target = surface.rect.center = MusicKit.Targets.HIDDEN

        self.surface = surface
        self.render = surface.render
        self.active = False

        self.fillRect = pg.Rect((0, 0), self.size)
        self.old_x = self.pos[0]

        self.paddle = paddle
        self.PauseMenu = pause_menu

        self.TrackText = Text(self.render, (0, 0), "Track text", ("koulen", 20), Colors.BLACK)
        self.generate_text()

        self.PaddleYTargets = {
            "default": paddle.pos.y,
            "upper": paddle.pos.y - MusicKit.Default.PADDLE_BOUNCE,
        }

        App.AudioS.sign_event(Command(self.generate_text))

    def generate_text(self):
        self.TrackText.value = (f"{App.AudioS.CurrentTrack.name} "
                                f"{App.AudioS.CurrentTrack.info('artist', 'Unknow')[0]}")
        self.TrackText.rect.center = self.size[0] / 2, self.size[1] / 2


    def switch_active(self, active: bool):

        if self.active == active:
            return

        self.toggle_active()

    def toggle_active(self):
        if self.active:
            self.target = MusicKit.Targets.HIDDEN
            self.active = False

        else:
            self.target = MusicKit.Targets.ACTIVE
            self.active = True

    def update(self):
        self.surface.rect.y = lerp(self.surface.rect.y, self.target[1], 0.1)

        self.switch_active(App.AudioS.progress < MusicKit.Default.FADEOUT)

        if self.active and self.pos[0] < self.paddle.pos.x + self.paddle.hitbox.size[0] and \
                self.pos[0] + self.size[0] > self.paddle.pos.x:
            self.paddle.target_y = self.PaddleYTargets["upper"]
        elif not self.PauseMenu.active:
            self.paddle.target_y = self.PaddleYTargets["default"]


    @property
    def pos(self):
        return self.surface.rect.topleft

    @property
    def size(self):
        return self.surface.rect.size


    def draw(self):

        with self.surface.capture():

            self.render.draw_color = MusicKit.Default.FILLER_COLOR.rgba
            percentage = App.AudioS.progress / MusicKit.Default.FADEOUT
            self.fillRect.w = self.size[0] * percentage
            self.render.fill_rect(self.fillRect)

            self.TrackText.draw()

        self.surface.rect.x = self.old_x - MusicKit.Default.OFFSET_X * percentage

        self.surface.draw()
        self.surface.clear(MusicKit.Default.BG_COLOR.rgba)





def main():
    pass


if __name__ == "__main__":
    main()
