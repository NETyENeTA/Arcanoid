import Libraries.SimplePyGame.Screen as ScreenLib
from Libraries.SimplePyGame.Audio.AudioSystem import AudioSystem
from Libraries.SimplePyGame.Audio.SFXSystem import SFXSystem
import pygame as pg

import GameFiles.Configs.WindowApp as WindowConfig
from Libraries.SimplePyGame.SDL2.Text.FontSystem import FontSystem
from core.GameElements.Systems.LightSystem import LightSystem

from core.GameElements.Cursor import Cursor


class Resolution:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height

    @property
    def W(self):
        return self.__width

    @property
    def H(self):
        return self.__height

    @property
    def WH(self):
        return self.__width, self.__height

class FPSCounter:
    def __init__(self, sample_size=100):
        self.sample_size = sample_size
        self.frames = []

    def tick(self):
        self.frames.append(AppConfigs.Clock.get_fps())
        if len(self.frames) > self.sample_size:
            self.frames.pop(0)

    @property
    def avg(self):
        if not self.frames: return 0
        return sum(self.frames) / len(self.frames)


class AppConfigs:
    Resolution: Resolution = Resolution(*WindowConfig.RESOLUTION)
    Screen: ScreenLib.Screen = None
    FontS: FontSystem = None

    AudioS: AudioSystem = None
    sfx: SFXSystem = None

    Clock: pg.time.Clock
    FPS = WindowConfig.FPS

    Cursor: Cursor = None

    FPSCounter = FPSCounter()

    cheat: str  = ""

    cheats: list[str] = [
        "add ball", "add score",
        "debug", "debugging", "bounce-up", "bounce-down", "help"
    ]

    dt: float = 0

    class Runtime:
        IsOn: bool
        IsError: bool
        IsCriticalError: bool
        IsPause: bool

        IsDebugging: bool
        IsDebug: bool

    class ControlMode:
        Keyboard = 0
        Mouse = 1


    LightS: LightSystem = None
    CurrentController: int = ControlMode.Keyboard

    @staticmethod
    def ticks():
        return pg.time.get_ticks()

    @staticmethod
    def seconds():
        return pg.time.get_ticks() / 1000




    @staticmethod
    def toggle_pause():
        AppConfigs.Runtime.IsPause = not AppConfigs.Runtime.IsPause

    @staticmethod
    def events():
        return pg.event.get()

    @staticmethod
    def flip():
        AppConfigs.Screen.render.present()
        # pg.display.flip()

    @staticmethod
    def clear(color: tuple[int, int, int]):
        AppConfigs.Screen.render.draw_color = color
        AppConfigs.Screen.render.clear()


    @staticmethod
    def stop():
        print("Stopping")
        AppConfigs.Runtime.IsOn = False

    @staticmethod
    def keys():
        return pg.key.get_pressed()

    @staticmethod
    def tick(fps=FPS):
        # Получаем время в секундах
        raw_dt = AppConfigs.Clock.tick(fps) / 1000.0

        # Ограничиваем dt (например, не больше 0.1 секунды)
        # Это спасет от "пролетов" сквозь текстуры при лагах
        AppConfigs.dt = min(raw_dt, 0.1)

    @staticmethod
    def date_time():
        return AppConfigs.dt

