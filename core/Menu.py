from Libraries.Python.Command import Command
from Libraries.SimplePyGame.Colors import Colors
from Libraries.SimplePyGame.Positions import Vec2
from Libraries.SimplePyGame.SDL2.UI.Button import Button
from core.App import AppConfigs as App

import pygame as pg

from core.Game import Game
from core.App import AppConfigs as App, WindowConfig as WC


class Menu:

    BG_COLOR = Colors.WHITE

    @staticmethod
    def hello():
        print("Hello, World!")

    def continue_game(self):
        self.Game.run()

    def new_game(self):
        self.Game = Game(self.screen, self.render)
        self.continue_game()

    def __init__(self, screen, render):
        self.screen = screen
        self.render = render

        self.On = True

        self.Game = Game(screen, render)

        self.buttons = [
            Button((10, 10), (230, 40), Colors.BLACK, command=Command(self.new_game)),
            Button((10, 10), (230, 40), Colors.BLACK, command=Command(self.continue_game)),
            Button((10, 10), (230, 40), Colors.BLACK, command=Command(self.exit)),
        ]


        self.buttons[0].hitbox.center = (Vec2(0, -60) + WC.Center).xy
        self.buttons[1].hitbox.center = WC.Center
        self.buttons[2].hitbox.center = (Vec2(0, 60) + WC.Center).xy

    def exit(self):
        self.On = False

    def update(self):
        while self.On:
            App.tick()

            self.events()
            self.display()

    def events(self):
        for event in App.events():
            if event.type == pg.QUIT:
                self.On = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.events()

    def display(self):
        App.clear(Menu.BG_COLOR.rgb)


        for button in self.buttons:
            button.draw()


        App.flip()


    def run(self):
        self.On = True
        self.update()






