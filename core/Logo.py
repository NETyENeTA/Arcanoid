from Libraries.SimplePyGame.Colors import Colors
from core.App import AppConfigs as App, pg

class Logo:

    BG_COLOR = Colors.WHITE

    def __init__(self, screen, render):

        self.screen = screen
        self.render = render

        self.On : bool = True



    def update(self):
        while self.On:

            App.tick()

            self.events()
            self.display()



    def events(self):

        for event in App.events():
            if event.type == pg.QUIT:
                self.On = False


    def display(self):
        App.clear(Logo.BG_COLOR.rgb)


        App.flip()


    def run(self):
        self.On = True
        self.update()