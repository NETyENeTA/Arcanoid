from Libraries.SimplePyGame.Positions import Vec2
from core.App import AppConfigs as App, pg
import GameFiles.Configs.WindowApp as WC
from Libraries.SimplePyGame.Colors import Colors
from Libraries.SimplePyGame.Color import Color

from Libraries.SimplePyGame.SDL2.Gradient import Gradient

from Libraries.SimplePyGame.SDL2.Draw import draw_line, draw_horizontal_line


class HUD:
    Damage_timer = 0
    Is_damaged = False

    def __init__(self):
        self.render = App.Screen.render

        test_rect = pg.Rect((0, 0), (WC.right - WC.Right, 50))
        test_rect.bottomleft = WC.bottom_left_gradient
        self.test_rect = test_rect

        self.gradients = [
            Gradient(self.render, test_rect, Gradient.Modes.Vertical, Colors.WHITE_Alpha_0,
                     Color(255, 50, 50, 255),
                     Color(255, 30, 30)),

            Gradient(self.render, test_rect, Gradient.Modes.Vertical, Colors.WHITE_Alpha_0,
                     Color.mono_color_with_alpha(150, 255),
                     Colors.BLACK)

        ]

        self.gradient = self.gradients[1]
        self.top_rect = pg.Rect((WC.Right, 0), (WC.right - WC.Right, WC.Top))
        self.bottom_rect = pg.Rect(WC.bottom_left, (WC.right - WC.Right, WC.Bottom))
        self.left_rect = pg.Rect((0, 0), (WC.Right, WC.H))
        self.right_rect = pg.Rect((WC.right, 0), (WC.Left, WC.H))

    @staticmethod
    def visualisate_damage():
        HUD.Is_damaged = True
        HUD.Damage_timer = 0.5  # Эффект длится 0.5 секунды

    def update(self):

        if HUD.Is_damaged:
            HUD.Damage_timer -= App.dt
            if HUD.Damage_timer <= 0:
                HUD.Is_damaged = False
                self.gradient = self.gradients[1] # Возвращаем черный
            else:
                self.gradient = self.gradients[0] # Держим красный


    def draw(self):

        self.render.draw_color = Colors.WHITE.rgb

        # self.render.draw_color = Colors.RED.rgb
        self.render.fill_rect(self.top_rect)
        self.render.fill_rect(self.bottom_rect)

        # self.render.draw_color = Colors.GREEN.rgb
        self.render.fill_rect(self.left_rect)
        self.render.fill_rect(self.right_rect)

        # self.render.draw_color = Colors.BLACK.full
        # draw_line(self.render, WC.Audio_Left, WC.Audio_Right, WC.Audio_thickness, Colors.GRAY)
        draw_horizontal_line(self.render, WC.Audio_left, WC.Audio_right, WC.Audio_Y, WC.Audio_thickness, Colors.GRAY)

        x = WC.Audio_total_width * App.AudioS.CurrentTrack.progress + WC.Audio_left
        draw_horizontal_line(self.render, WC.Audio_left, x, WC.Audio_Y, WC.Audio_thickness, Colors.BLACK)

        self.gradient.blit()

        self.render.draw_color = Colors.BLACK.rgb
        draw_line(self.render, WC.top_left, WC.bottom_left, 3)
        draw_line(self.render, WC.top_right, WC.bottom_right, 3)
        draw_line(self.render, WC.top_left, WC.top_right, 3)
        draw_line(self.render, WC.bottom_left, WC.bottom_right, 3)






        # App.FontS.draw_text(f"FPS: {int(App.Clock.get_fps())} dt: {App.dt}", "prstart.ttf", size=18,
        #                     pos=Vec2(WC.Center[0], 10))


