from Colors import Colors
from Event.CommandStuff.Command import Command
from Positions import Vec2
from Text.Text import Text


class InteractiveButton:

    def __init__(self, pos: Vec2, text: Text, command: Command, selected: bool = False, disabled: bool = False):
        self.text = text
        self.pos = pos
        self.selected = selected
        self.disabled = disabled

        self.command = command


    def draw(self):
        self.text.draw()

    @property
    def disabled(self):
        return self.__disabled

    @disabled.setter
    def disabled(self, value):
        self.__disabled = value
        self.text.color = Colors.BLACK_RED if value else Colors.BLACK


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
