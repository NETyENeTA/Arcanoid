from Libraries.SimplePyGame.Color import Color, NameSpaces as ColorNameSpaces
from Libraries.SimplePyGame.SDL2.Text.FontInfo import FontInfo
from Libraries.SimplePyGame.Positions import Vec2, PositionObject

from core.App import AppConfigs as App


class DynamicText(PositionObject):

    def __init__(self, pos: Vec2 | tuple, value, font: FontInfo | tuple[str, int] | dict, color: Color
                 | ColorNameSpaces.color, visible: bool = True):
        super().__init__(pos)

        self.font = font if isinstance(font, FontInfo) else (FontInfo.from_dict(font) if
                                                             isinstance(font, dict) else FontInfo.from_sequence(font))
        self.color = color if isinstance(color, Color) else Color(color)
        self.value = value
        self.is_visible = visible

    def draw(self):

        if not self.is_visible:
            return

        App.FontS.draw_text(self.value, self.font.name, self.font.size, self.color.rgba, self.pos)
