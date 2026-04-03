# from sys import flags

import Game as GameCore

import pygame as pg
from pygame._sdl2 import Window, Renderer

from Libraries.SimplePyGame.Audio.AudioSystem import AudioSystem
from Libraries.SimplePyGame.Audio.SFXSystem import SFXSystem
from Libraries.SimplePyGame.SDL2.Text.FontSystem import FontSystem
from Libraries.SimplePyGame.UI.Mouse import Mouse
from core.App import AppConfigs, ScreenLib, WindowConfig as WC
from core.GameElements.Cursor import Cursor
from core.GameElements.Systems.LightSystem import LightSystem

from os.path import dirname, join, abspath

class Application:


    RUN_DIR = dirname(abspath(__file__))
    BASE_DIR = dirname(RUN_DIR)
    FONTS_DIR = join(BASE_DIR, "GameFiles", "Media", "fonts")

    def __init__(self):
        print("Hello, World!")

        AppConfigs.Runtime.IsError = False
        AppConfigs.Runtime.IsCriticalError = False
        AppConfigs.Runtime.IsPause = False

        self.debbuger()

        # flags = pg.RESIZABLE | pg.SCALED
        # sc = pg.display.set_mode(AppConfigs.Resolution.WH, flags=flags)
        sc = Window("Arcanoid2", size=AppConfigs.Resolution.WH)
        render = Renderer(sc, vsync=WC.vsync)

        AppConfigs.Screen = ScreenLib.Screen(sc=sc, render=render)
        self.sc = sc
        self.render = render

        AppConfigs.Clock = pg.time.Clock()

        AppConfigs.LightS = LightSystem()
        AppConfigs.AudioS = AudioSystem()

        AppConfigs.Cursor = Cursor(self.render)


        self.sfx()
        self.fonts()

        Mouse.set_cursor_visibility(False)
        self.Game = GameCore.Game(sc, render)

    def sfx(self):
        AppConfigs.sfx = SFXSystem(AppConfigs.Resolution.W)
        AppConfigs.sfx.load("ball hit", "../GameFiles/Media/audio/sounds/sfx/ball_hit.wav")
        AppConfigs.sfx.load("ball hit a default block", "../GameFiles/Media/audio/sounds/sfx/explosion.wav")


    def fonts(self):
        AppConfigs.FontS = FontSystem(self.render)
        # AppConfigs.FontS.add("Main", "GameFiles/Media/fonts/", "pixel.ttf", size=30)

        AppConfigs.FontS.add("koulen", self.FONTS_DIR, 12, "Koulen.ttf")
        AppConfigs.FontS.add("blox2", self.FONTS_DIR, 12, "Blox2.ttf")
        AppConfigs.FontS.add("prstart", self.FONTS_DIR, 12, "prstart.ttf")

    def debbuger(self):
        AppConfigs.Runtime.IsDebugging = False
        AppConfigs.Runtime.IsDebug = True



    def start(self):
        AppConfigs.Runtime.IsOn = True
        self.Game.run()
