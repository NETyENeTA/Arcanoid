# Python Lib
from DateTime.Task import Task
from Event.Event import Event
from Event.CommandStuff.Command import Command
from Libraries.Python.List import get_at

# SPG Lib
from Libraries.SimplePyGame.Colors import Colors
from Libraries.SimplePyGame.Color import Color

from Libraries.SimplePyGame.DateTime.Timer import Timer
from Libraries.SimplePyGame.DateTime.TimerExecuteable import TimerExecutable
from Libraries.SimplePyGame.Positions import Vec2
from Libraries.SimplePyGame.UI.Mouse import Mouse

from Libraries.SimplePyGame.SDL2.Text.Text import Text

# Configs & Settings
import GameFiles.Settings.Player as PS
import GameFiles.Configs.WindowApp as WC

from core.GameElements.MusicKit import MusicKit
from core.GameElements.PauseMenu import PauseMenu
from core.GameElements.Systems.GunSystem import GunSystem

# core.GameElements
# todo: check if need to delete prefix: "core."
from core.GameElements.HUD import HUD
from core.GameElements.Paddle import Paddle

from core.GameElements.Systems.BallSystem import BallSystem
from core.GameElements.Systems.BonusSystem import BonusSystem
from Items.Block.Block import Block
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

    def restart(self):
        App.Runtime.IsPause = False
        self.Stopwatch.Tasks.clear()
        Command.clear_tasks()
        self.__init__(self.sc, self.render)

    def start_next_game(self):
        for text in self.Texts:
            text.is_visible = False

        text = self.Texts[4]
        text.value = "Get Ready!!!"
        text.is_visible = True
        Command(self.next_level, 3, text).invoke(timeout=3)


    def next_level(self, counter, text: Text):

        if counter < 0:
            self.restart()
            return

        text.value = f"{counter}"
        text.rect.center = WC.Center

        Command(self.next_level, counter - 1, text).invoke(timeout=3)

    def __init__(self, screen, render):
        print("Initializing Game")
        self.sc = screen
        self.render = render

        self.status = Game.Status.Playing

        # App.LightS.add(Vec2(WC.Center_left_box[0], WC.bottomLights), Colors.BLUE, render)
        App.LightS.add(Vec2(WC.Center[0], WC.bottomLights), Colors.GRAY, render)
        # App.LightS.add(Vec2((WC.Center_right_box[0], WC.bottomLights), 610), Colors.RED, render)

        self.Stopwatch = TimerExecutable(60*4, pause=True, command=self.end_game, tasks=
        [
            Task(30, Command(self.red_seconds, loops=0, delay=1.5), True)
        ])

        self.player: Paddle = Paddle(
            (App.Resolution.W // 2, App.Resolution.H - PS.Offset_collision[1]),
            (240, 30),
            Colors.BLACK, self.Stopwatch)

        self.player.shadow_info.minimal = 15

        # todo: Add normal class for Colors of block
        test_blocks = [
            Block(Vec2(i * 110 + 90, j * 50 + 90), Vec2(100, 35), None, None,
                  Color.mono_color_alpha(150), Color.mono_color_alpha(100),
                  Color.mono_color_alpha(0), Color.mono_color_alpha(150))
            for i in range(13) for j in range(5)
        ]

        level2 = [
            Block(Vec2(i * 110 - 30, j * 50 + 90), Vec2(100, 35), None, None,
                  Color.mono_color_alpha(150), Color.mono_color_alpha(100),
                  Color.mono_color_alpha(0), Color.mono_color_alpha(150))
            for i in range(14)
            for j in range(i if i <= 8 else 8)
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
        self.BonusS = BonusSystem(self.player, self.add_ball, self.add_sticky_ball, self.rise_speed_ball,
                                  self.activate_any_gun)
        self.BlockS = BlockSystem(self.BonusS, test_blocks)
        self.GunS = GunSystem(self.player, self.BlockS, self.pass_level)
        self.BallS = BallSystem(self.player, self.BlockS, self.end_game, self.pass_level)

        self.Texts = [
            Text(self.render, Vec2(0, 0), "Tutorial", ("prstart", 48), Color.mono_color(150).rgb),
            Text(self.render, Vec2(0, 0), "Game Over", ("prstart", 48), Color.mono_color(0).rgb,
                 False),
            Text(self.render, Vec2(0, 0), "Value", ("prstart", 24), Color.mono_color(0).rgb,
                 False),
            Text(self.render, Vec2(0, 0), "Level Passed", ("prstart", 48), Color.mono_color(0).rgb,
                 False),
            Text(self.render, Vec2(0, 0), "Get Ready!", ("prstart", 48), Color.mono_color(0).rgb,
                 False),
        ]

        self.Texts[0].rect.center = (Vec2(0, 60) + WC.Center).xy
        self.Texts[1].rect.center = (Vec2(0, 30) + WC.Center).xy
        self.Texts[2].rect.center = (Vec2(0, 70) + WC.Center).xy
        self.Texts[3].rect.center = (Vec2(0, 30) + WC.Center).xy
        self.Texts[4].rect.center = WC.Center

        self.PauseMenu = PauseMenu(self.player, self.restart)
        self.MusicKit = MusicKit(self.player, self.PauseMenu)

    def red_seconds(self):
        self.player.RedSecs = Paddle.Default.RedSecs

    def activate_any_gun(self):
        self.GunS.activate_gun()

    def rise_speed_ball(self):
        self.BallS.rise_speed()


    def add_sticky_ball(self, radius=14):
        self.BallS.add((
            self.player.hitbox.centerx,
            self.player.hitbox.top - radius
        ), radius)

    def add_ball(self, radius=14):
        pos = self.BallS.Balls[-1].pos
        self.BallS.add(pos, radius, False)

    def pass_level(self):

        self.BallS.is_passed_level = True

        self.Stopwatch.switch_pause(True)

        self.status = Game.Status.PassedLevel
        self.Texts[2].value = self.player.info
        self.Texts[2].rect.center = (Vec2(0, 70) + WC.Center).xy

        self.Texts[0].is_visible = False
        self.Texts[2].is_visible = True
        self.Texts[3].is_visible = True

        self.PauseMenu.InteractiveBtns[0].disabled = True

        Command(self.start_next_game).invoke(timeout=4)

    def kill_player(self):
        self.player.health -= 1

    def end_game(self):

        self.PauseMenu.switch_active(True)
        self.Stopwatch.switch_pause(True)

        self.BallS.is_end_game = True
        # self.player.health = -1
        Command(self.kill_player).invoke(loops=self.player.health + 1, timeout=0.2)

        self.status = Game.Status.GameOver
        self.Texts[2].value = self.player.info
        self.Texts[2].rect.center = (Vec2(0, 70) + WC.Center).xy

        for i in range(3):
            self.Texts[i].is_visible = not self.Texts[i].is_visible

    def update(self):
        Mouse.set_cursor_visibility(False)
        while App.Runtime.IsOn:
            App.tick()
            App.FPSCounter.tick()
            App.AudioS.update()
            # App.Screen.screen.title = f"FPS:{int(App.Clock.get_fps())} AVG:{int(App.FPSCounter.avg)}, dt:{App.dt}"

            Command.update_schedule()
            if self.status == Game.Status.Playing:
                self.Stopwatch.update()

            self.events()
            self.PauseMenu.update()
            self.MusicKit.update()
            if App.Runtime.IsPause:
                self.player.update_bounce()
                self.BallS.update_sticky()
            else:
                # Debug, light to mouse
                if App.Runtime.IsDebugging:
                    # App.LightS.Lights[0].pos = Mouse.pos()
                    self.BallS.Balls[0].hitbox.center = Mouse.pos().xy

                self.player.update()
                self.GunS.update()
                self.BlockS.update()
                self.BonusS.update()
                self.BallS.update()
                self.HUD.update()

            self.display()

        Mouse.set_cursor_visibility(True)

    def check_cheat(self):

        if App.cheat == App.cheats[0]:
            self.BallS.add(Vec2(400, 800), 14)
            self.BallS.Balls[0].direction.xy = (0, 1)

        if App.cheat == App.cheats[1]:
            self.player.add_score(50)

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

            elif event.type == Event.Types.EXECUTE_COMMAND:
                command = event.dict.get(Command.Default.MY_NAME)
                if command:
                    command()

            elif event.type == pg.KEYDOWN:

                # pg.mouse.set_visible(True)
                App.CurrentController = App.ControlMode.Keyboard
                if App.Runtime.IsPause:
                    if event.key not in (pg.K_RETURN, pg.K_TAB, pg.K_BACKSPACE):
                        App.cheat += event.unicode
                    if not any(cheat.startswith(App.cheat) for cheat in App.cheats):
                        App.cheat = ""

                if event.key == pg.K_ESCAPE:
                    # if self.player.is_alive:
                    #     App.toggle_pause()
                    # self.PauseMenu.toggle_active()
                    self.PauseMenu.toggle_pause(self.player.is_alive and not self.BallS.is_passed_level)
                    if self.status not in (Game.Status.GameOver, Game.Status.PassedLevel):
                        self.Stopwatch.toggle_pause()

                elif event.key == pg.K_RIGHT:
                    if self.PauseMenu.active:
                        self.PauseMenu.select += 1

                elif event.key == pg.K_LEFT:
                    if self.PauseMenu.active:
                        self.PauseMenu.select -= 1

                elif event.key == pg.K_BACKSPACE:
                    App.cheat = App.cheat[:-1]

                elif event.key == pg.K_SPACE:
                    self.player.started = True
                    App.realSpacePressed = True
                    if not App.Runtime.IsPause:
                        self.Stopwatch.switch_pause(False)
                    if not self.BonusS.is_check_bonus_in(BonusSystem.Types.ADD_STICKY_BALL):
                        self.BonusS.is_stickyBall_here = False

                elif event.key == pg.K_TAB:
                    print(event)
                    if App.cheat:
                        self.auto_complete()
                    elif event.mod == 1:
                        App.AudioS.play_prev()
                    else:
                        App.AudioS.play_next()

                elif event.key == pg.K_RETURN:
                    if App.cheat:
                        self.check_cheat()
                    elif self.PauseMenu.active:
                        self.PauseMenu.check_buttons()

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
        self.GunS.draw()

        self.BallS.draw()
        self.BlockS.draw()
        self.BonusS.draw()

        self.PauseMenu.draw()
        self.MusicKit.draw()
        App.Cursor.draw_center()

        self.HUD.draw()

        if App.Runtime.IsDebug and App.Runtime.IsPause:
            matches = self.get_matches()
            helper = [cheat for cheat in App.cheats if cheat != 'help' or cheat != App.cheat] \
                if App.cheat == "help" else matches

            if App.cheat == "help":
                helper[0] = f" {helper[0]}"

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
