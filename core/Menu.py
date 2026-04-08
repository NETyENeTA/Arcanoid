from Event.CommandStuff.Command import Command
from Libraries.SimplePyGame.Color import Color
from Libraries.SimplePyGame.Colors import Colors
from Libraries.SimplePyGame.Positions import Vec2
from Libraries.SimplePyGame.SDL2.Text.Text import Text
from Libraries.SimplePyGame.SDL2.UI.ButtonColors import ButtonColors
from Libraries.SimplePyGame.SDL2.UI.TextButton import TextButton
from Libraries.SimplePyGame.SDL2.UI.TextButtonColors import TextButtonColors

import pygame as pg

from core.Game import Game
from core.App import AppConfigs as App, WindowConfig as WC


class Menu:

    BG_COLOR = Colors.WHITE

    @staticmethod
    def hello():
        print("Hello, World!")

    def continue_game(self):
        self.Game.continue_game()

    def new_game(self):
        self.Game = Game(self.screen, self.render)
        self.Game.run()
        self.buttons[1].switch(False)

    def __init__(self, screen, render):
        self.screen = screen
        self.render = render

        self.On = True
        self.Game: Game | None = None

        App.AudioS.volume = 0

        btn_color = ButtonColors(
            Colors.BLACK,
            Colors.GRAY,
            Color.mono_color(170),
            Colors.GRAY
        )

        text_color = TextButtonColors(
            Colors.WHITE,
            Colors.BLACK,
            Colors.BLACK,
            Colors.BLACK
        )

        self.texts = [
            Text(self.render, (0, 0), "Arcanoid", ("prstart", 32), Colors.BLACK.rgb),
            Text(self.render, (0, 0), "base on pg_ce.sdl2", ("koulen", 20), Colors.BLACK.rgb),
        ]

        self.texts[0].rect.centerx, self.texts[0].rect.bottom = WC.Center[0], WC.Center[1] - 150
        self.texts[1].rect.centerx, self.texts[1].rect.bottom = WC.Center[0], WC.Center[1] - 120

        self.buttons = [
            TextButton((10, 10), (230, 40), "new game", ("prstart", 12),
                       btn_color, text_color, command=Command(self.new_game), ),

            TextButton((10, 10), (230, 40), "continue game", ("prstart", 12),
                       btn_color, text_color, command=Command(self.continue_game), disabled=True),

            TextButton((10, 10), (230, 40), "exit", ("prstart", 12),
                       btn_color, text_color, command=Command(self.exit), )
        ]


        self.buttons[0].hitbox.center = (Vec2(0, -60) + WC.Center).xy
        self.buttons[1].hitbox.center = WC.Center
        self.buttons[2].hitbox.center = (Vec2(0, 60) + WC.Center).xy

    def exit(self):
        self.On = False

    def update(self):
        while self.On:
            App.tick()
            App.AudioS.update()

            self.events()
            self.display()

    def events(self):
        for event in App.events():
            if event.type == pg.QUIT:
                self.On = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.press()

            elif event.type == pg.MOUSEBUTTONUP:
                for button in self.buttons:
                    button.invoke()

    def display(self):
        App.clear(Menu.BG_COLOR.rgb)

        for text in self.texts:
            text.draw()

        for button in self.buttons:
            button.draw()


        App.flip()


    def run(self):
        self.On = True
        self.update()






