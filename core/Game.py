from Libraries.Python.List import get_at
from Libraries.SimplePyGame.Color import Color
from Libraries.SimplePyGame.DateTime.Timer import Timer
from core.App import AppConfigs as App, pg
from GameElements.Paddle import Paddle
from core.GameElements.HUD import HUD

from Libraries.SimplePyGame.Colors import Colors
from Libraries.SimplePyGame.Positions import Vec2

import GameFiles.Settings.Player as PS
import GameFiles.Configs.WindowApp as WC

from core.GameElements.Systems.BallSystem import BallSystem
from core.GameElements.SystemItems.Block import Block
from core.GameElements.Systems.BlockSystem import BlockSystem

from Libraries.SimplePyGame.UI.Mouse import Mouse


class Game:
    BgColor = Colors.WHITE

    def __init__(self, screen, render):
        print("Initializing Game")
        self.sc = screen
        self.render = render

        # App.LightS.add(Vec2(WC.Center_left_box[0], WC.bottomLights), Colors.BLUE, render)
        App.LightS.add(Vec2(WC.Center[0], WC.bottomLights), Colors.GRAY, render)
        # App.LightS.add(Vec2((WC.Center_right_box[0], WC.bottomLights), 610), Colors.RED, render)

        self.Timer = Timer()

        self.player: Paddle = Paddle(
            (App.Resolution.W // 2, App.Resolution.H - PS.Offset_collision[1]),
            (240, 30),
            Colors.BLACK, self.Timer)

        self.player.shadow_info.minimal = 15

        test_blocks = [
            Block(Vec2(i * 110 + 90, j * 50 + 90), Vec2(100, 35), None, None,
                  Color.mono_color_alpha(150), Color.mono_color_alpha(100),
                  Color.mono_color_alpha(0))
            for i in range(13) for j in range(5)
        ]

        test_block = [
            Block(Vec2(90, 90), Vec2(1400, 300), None, None,
                  Color.mono_color_alpha(150), Color.mono_color_alpha(100),
                  Color.mono_color_alpha(0))
        ]

        test_block[0].health = 3

        self.HUD: HUD = HUD()
        self.BlockS = BlockSystem(test_blocks)
        self.BallS = BallSystem(self.player, self.BlockS)

    def update(self):
        while App.Runtime.IsOn:
            App.tick()
            App.FPSCounter.tick()
            App.AudioS.update()
            # App.Screen.screen.title = f"FPS:{int(App.Clock.get_fps())} AVG:{int(App.FPSCounter.avg)}, dt:{App.dt}"

            self.events()
            if not App.Runtime.IsPause:

                # Debug, light to mouse
                if App.Runtime.IsDebugging:
                    App.LightS.Lights[0].pos = pg.mouse.get_pos()

                self.player.update()
                self.BallS.update()
                self.HUD.update()

            self.display()

    def chack_cheat(self):

        if App.cheat == App.cheats[0]:
            self.BallS.add(Vec2(400, 800), 14)
            self.BallS.Balls[0].direction.xy = (0, 1)

        if App.cheat == App.cheats[1]:
            self.player.score += 10

        if App.cheat == App.cheats[2]:
            App.Runtime.IsDebug = not App.Runtime.IsDebug

        if App.cheat == App.cheats[3]:
            App.Runtime.IsDebugging = not App.Runtime.IsDebugging

        # Warn: its just debug need to delete in soon
        if App.cheat == App.cheats[4]:
            self.player.bounce(-20)

        if App.cheat == App.cheats[5]:
            self.player.bounce(20)

        if App.cheat in App.cheats:
            App.cheat = ""

    @staticmethod
    def get_matches():
        if len(App.cheat) == 0:
            return []
        return [cheat for cheat in App.cheats if cheat.startswith(App.cheat)]

    def auto_complete(self):
        matches = self.get_matches()
        if matches:
            App.cheat = matches[0]

    def events(self):

        for event in App.events():
            if event.type == pg.QUIT:
                App.stop()  # exiting
            elif event.type == pg.KEYDOWN:

                # pg.mouse.set_visible(True)
                App.CurrentController = App.ControlMode.Keyboard
                if App.Runtime.IsPause:
                    if event.key not in (pg.K_RETURN, pg.K_TAB, pg.K_BACKSPACE):
                        App.cheat += event.unicode
                    if not any(cheat.startswith(App.cheat) for cheat in App.cheats):
                        App.cheat = ""

                if event.key == pg.K_ESCAPE:
                    App.toggle_pause()
                    self.Timer.toggle_pause()

                elif event.key == pg.K_BACKSPACE:
                    App.cheat = App.cheat[:-1]

                elif event.key == pg.K_TAB:
                    self.auto_complete()

                elif event.key == pg.K_TAB:
                    App.AudioS.play_next()

                elif event.key == pg.K_RETURN:
                    self.chack_cheat()

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 3:
                    print(Mouse.pos())

            elif event.type == pg.MOUSEMOTION:
                # Если двинули или кликнули — скрываем мышь, переходим в режим мыши
                if pg.mouse.get_focused():
                    # pg.mouse.set_visible(False)
                    App.CurrentController = App.ControlMode.Mouse

    def display(self):
        App.clear(Game.BgColor.rgba)

        self.BlockS.cast_shadows()
        self.BallS.cast_shadows()
        self.player.cast_shadow()

        self.player.draw()

        self.BallS.draw()
        self.BlockS.draw()

        App.Cursor.draw_center()

        self.HUD.draw()

        if App.Runtime.IsDebug and App.Runtime.IsPause:

            matches = self.get_matches()
            helper = [cheat for cheat in App.cheats if cheat != 'help' or cheat != App.cheat]\
                if App.cheat == "help" else matches

            # print(helper, App.cheat, get == App.cheat)

            App.FontS.draw_text(
                text=" \n ".join(helper),
                name="koulen",
                size=20,
                color=(150, 150, 150),
                pos=(WC.debug_matches[0], WC.debug_matches[1] - len(matches) * 10 - len(helper) * 30),
            )


            App.FontS.draw_text(
                text=f"{get_at(matches, 0, 'Type something, cheat engine 1.0')}",
                name="koulen",
                size=20,
                color=(150, 150, 150),
                pos=WC.debug_text
            )


            App.FontS.draw_text(
                text=f"{App.cheat}",
                name="koulen",
                size=20,
                color=(0, 0, 0),
                pos=WC.debug_text
            )

        if App.Runtime.IsDebugging:
            App.LightS.draw_debug()

        App.flip()

    def run(self):
        print("Start Game")
        self.update()
