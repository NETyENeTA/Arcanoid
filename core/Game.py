# Python Lib
from Libraries.Python.List import get_at

# SPG Lib
from Libraries.SimplePyGame.Colors import Colors
from Libraries.SimplePyGame.Color import Color

from Libraries.SimplePyGame.DateTime.Timer import Timer
from Libraries.SimplePyGame.Positions import Vec2
from Libraries.SimplePyGame.UI.Mouse import Mouse

from Libraries.SimplePyGame.SDL2.Text.Text import Text

# Configs & Settings
import GameFiles.Settings.Player as PS
import GameFiles.Configs.WindowApp as WC

# core.GameElements
# todo: check if need to delete prefix: "core."
from core.GameElements.HUD import HUD
from core.GameElements.Paddle import Paddle

from core.GameElements.Systems.BallSystem import BallSystem
from core.GameElements.Systems.BonusSystem import BonusSystem
from core.GameElements.Systems.Items.Block import Block
from core.GameElements.Systems.BlockSystem import BlockSystem

# Warn!!! "core." is required!!!
from core.App import AppConfigs as App, pg


class Game:
    BgColor = Colors.WHITE

    class Status:

        PassedLevel = 2
        Playing = 1
        Death = 0
        GameOver = -1

    def __init__(self, screen, render):
        print("Initializing Game")
        self.sc = screen
        self.render = render

        self.status = Game.Status.Playing

        # App.LightS.add(Vec2(WC.Center_left_box[0], WC.bottomLights), Colors.BLUE, render)
        App.LightS.add(Vec2(WC.Center[0], WC.bottomLights), Colors.GRAY, render)
        # App.LightS.add(Vec2((WC.Center_right_box[0], WC.bottomLights), 610), Colors.RED, render)

        self.Timer = Timer()

        self.player: Paddle = Paddle(
            (App.Resolution.W // 2, App.Resolution.H - PS.Offset_collision[1]),
            (240, 30),
            Colors.BLACK, self.Timer)

        self.player.shadow_info.minimal = 15

        # todo: Add normal class for Colors of block
        test_blocks = [
            Block(Vec2(i * 110 + 90, j * 50 + 90), Vec2(100, 35), None, None,
                  Color.mono_color_alpha(150), Color.mono_color_alpha(100),
                  Color.mono_color_alpha(0), Color.mono_color_alpha(150))
            for i in range(13) for j in range(5)
        ]

        test_block = [
            Block(Vec2(90, 90), Vec2(1400, 300), None, None,
                  Color.mono_color_alpha(150), Color.mono_color_alpha(100),
                  Color.mono_color_alpha(0), Color.mono_color_alpha(150))
        ]

        rgb_test_block = [
            Block(Vec2(90, 90), Vec2(1400, 300), None, None,
                  Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW)
        ]

        test_block[0].health = 3

        self.HUD: HUD = HUD()
        self.BonusS = BonusSystem(self.player, self.add_ball, self.add_sticky_ball)
        self.BlockS = BlockSystem(self.BonusS, test_blocks)
        self.BallS = BallSystem(self.player, self.BlockS, self.end_game, self.pass_level)

        self.Texts = [
            Text(self.render, Vec2(0, 0), "Tutorial", ("prstart", 48), Color.mono_color(150).rgb),
            Text(self.render, Vec2(0, 0), "Game Over", ("prstart", 48), Color.mono_color(0).rgb,
                 False),
            Text(self.render, Vec2(0, 0), "Value", ("prstart", 24), Color.mono_color(0).rgb,
                 False),
            Text(self.render, Vec2(0, 0), "Level Passed", ("prstart", 48), Color.mono_color(0).rgb,
                 False),
        ]

        self.Texts[0].rect.center = (Vec2(0, 60) + WC.Center).xy
        self.Texts[1].rect.center = (Vec2(0, 30) + WC.Center).xy
        self.Texts[2].rect.center = (Vec2(0, 70) + WC.Center).xy
        self.Texts[3].rect.center = (Vec2(0, 30) + WC.Center).xy

    def add_sticky_ball(self, radius=14):
        print("123")
        self.BallS.add(Vec2.Zero, radius)

    def add_ball(self, radius=14):
        pos = self.BallS.Balls[-1].pos
        self.BallS.add(pos, radius, False)

    def pass_level(self):

        self.Timer.toggle_pause()

        self.status = Game.Status.PassedLevel
        self.Texts[2].value = self.player.info
        self.Texts[2].rect.center = (Vec2(0, 70) + WC.Center).xy

        self.Texts[0].is_visible = False
        self.Texts[2].is_visible = True
        self.Texts[3].is_visible = True

    def end_game(self):

        self.Timer.toggle_pause()

        self.status = Game.Status.GameOver
        self.Texts[2].value = self.player.info
        self.Texts[2].rect.center = (Vec2(0, 70) + WC.Center).xy

        for i in range(3):
            self.Texts[i].is_visible = not self.Texts[i].is_visible

    def update(self):
        while App.Runtime.IsOn:
            App.tick()
            App.FPSCounter.tick()
            App.AudioS.update()
            # App.Screen.screen.title = f"FPS:{int(App.Clock.get_fps())} AVG:{int(App.FPSCounter.avg)}, dt:{App.dt}"

            self.events()
            if not App.Runtime.IsPause:
                # Debug, light to mouse
                # if App.Runtime.IsDebugging:
                # App.LightS.Lights[0].pos = Mouse.pos()
                # self.BallS.Balls[0].hitbox.center = Mouse.pos().xy

                self.player.update()
                self.BlockS.update()
                self.BonusS.update()
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
                    if self.status not in (Game.Status.GameOver, Game.Status.PassedLevel):
                        self.Timer.toggle_pause()

                elif event.key == pg.K_BACKSPACE:
                    App.cheat = App.cheat[:-1]

                elif event.key == pg.K_TAB:
                    App.AudioS.play_next()

                elif event.key == pg.K_SPACE:
                    if not self.BonusS.is_check_bonus_in(BonusSystem.Types.ADD_STICKY_BALL):
                        self.BonusS.is_stickyBall_here = False

                elif event.key == pg.K_LSHIFT:
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

        for text in self.Texts:
            text.draw()

        self.BonusS.cast_shadows()
        self.BlockS.cast_shadows()
        self.BallS.cast_shadows()
        self.player.cast_shadow()

        self.player.draw()

        self.BallS.draw()
        self.BlockS.draw()
        self.BonusS.draw()

        App.Cursor.draw_center()

        self.HUD.draw()

        if App.Runtime.IsDebug and App.Runtime.IsPause:
            matches = self.get_matches()
            helper = [cheat for cheat in App.cheats if cheat != 'help' or cheat != App.cheat] \
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
            self.BallS.draw_debug()

        App.flip()

    def continue_game(self):
        print("continue game")
        App.Runtime.IsOn = True
        self.update()

    def run(self):
        print("Start new Game")
        App.Runtime.IsOn = True
        App.Runtime.IsPause = False
        self.update()
