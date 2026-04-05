from Libraries.SimplePyGame.SDL2.UI.ButtonColors import ButtonColors, Color


class TextButtonColors(ButtonColors):

    def __init__(self, default: Color, hover: Color, pressed: Color, disabled: Color):
        super().__init__(default, hover, pressed, disabled)


