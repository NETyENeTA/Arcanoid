from Libraries.SimplePyGame.Colors import Colors
from Libraries.SimplePyGame.DateTime.Timer import Timer
from Libraries.SimplePyGame.SDL2.Text.Text import Text
from core.App import AppConfigs as App, pg, WindowConfig as WC

from  Libraries.Animations.Functions.Lerp import lerp

class Logo:

    BG_COLOR = Colors.WHITE

    def __init__(self, screen, render):

        self.screen = screen
        self.render = render

        self.On : bool = True

        self.text = Text(self.render, (0,0), "LogoType", ("prstart", 32), Colors.BLACK.rgb)
        self.text.rect.centerx = WC.Center[0]

        self.Timer = 10



    def update(self):
        while self.On:

            App.tick()
            self.text.rect.centery = lerp(self.text.rect.centery, WC.Center[1], 0.025)

            self.Timer -= App.dt
            if self.Timer <= 0:
                self.On = False


            self.events()
            self.display()



    def events(self):

        for event in App.events():
            if event.type == pg.QUIT:
                self.On = False


    def display(self):
        App.clear(Logo.BG_COLOR.rgb)

        self.text.draw()

        App.flip()


    def run(self):
        self.On = True
        self.update()