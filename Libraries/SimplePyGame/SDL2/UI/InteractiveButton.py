from Event.CommandStuff.Command import Command
from Positions import Vec2
from Text.Text import Text


class InteractiveButton:

    def __init__(self, pos: Vec2, text: Text, command: Command, selected: bool = False):
        self.text = text
        self.pos = pos
        self.selected = selected

        self.command = command


    def draw(self):
        self.text.draw()

    @property
    def pos(self):
        return self.text.pos

    @pos.setter
    def pos(self, value):
        self.text.pos = value

def main():
    pass


if __name__ == "__main__":
    main()
