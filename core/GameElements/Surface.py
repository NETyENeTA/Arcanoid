from Libraries.SimplePyGame.Color import Color
from Libraries.SimplePyGame.Screen import Screen
from Libraries.SimplePyGame.Positions import Vec2
from core.GameElements.Rectangle import Rectangle, pg


class Surface(Rectangle):
    def __init__(self, pos: Vec2 | tuple[int, int], size: Vec2 | tuple[int, int],
                 screen: pg.Surface | Screen | None = None, converted: bool = False):
        super().__init__(pos, size, screen=screen, color=None)
        del self.color

        self.surface = pg.Surface(size.xy if isinstance(size, Vec2) else size)
        if converted:
            self.surface = self.surface.convert_alpha()

    def draw_rect(self, color: tuple[int, int, int] | tuple[int, int, int, int],
                  pos: tuple[int, int], size: tuple[int, int]):

        pg.draw.rect(self.surface, color, (pos[0], pos[1], size[0], size[1]))


    def blit(self):
        self.screen.blit(self.surface, self.pos.xy)



