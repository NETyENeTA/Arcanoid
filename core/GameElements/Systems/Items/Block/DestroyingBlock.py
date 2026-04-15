from pygame._sdl2.video import Renderer

from Libraries.SimplePyGame.Color import Color, NameSpaces
from Libraries.SimplePyGame.Colors import Colors
from Libraries.SimplePyGame.Positions import Range
from Libraries.SimplePyGame.SDL2.UI.Rectangle import Rectangle, pg
from Libraries.SimplePyGame.Screen import Screen
from core.GameElements.ShadowCaster import ShadowCaster


from core.App import AppConfigs as App
from Items.Block.Block import Block


class DestroyingBlock(Rectangle, ShadowCaster):

    def __init__(self, pos = None, size = None, color: Color | NameSpaces.color | None = None,
                 render: Renderer | Screen = None,
                 block: Block | None = None):

        if block:
            pos = block.pos
            size = block.hitbox.size
            color = block.color
            render = block.render


        Rectangle.__init__(self, pos, size, color if color else Colors.BLACK
                           , render)

        self.shadow_info = Range(2, 0.1, 30)
        self.init_shadow()

    @property
    def is_gone(self) -> bool:
        return self.hitbox.width <= 0 or self.hitbox.height <= 0

    def draw_shadow_shape(self, surf, color):
        # Рисуем прямоугольник во весь размер поверхности
        pg.draw.rect(surf, color, (0, 0, *self.hitbox.size), border_radius=4)

    def update(self):
        old_center = self.hitbox.center

        # Уменьшаем размер (например, на 100 пикселей в секунду)
        shrink_amount = 100 * App.dt
        new_w = max(0, self.hitbox.width - shrink_amount)
        new_h = max(0, self.hitbox.height - shrink_amount)

        self.hitbox.size = (new_w, new_h)
        # Возвращаем центр на место, чтобы блок не "уезжал"
        self.hitbox.center = old_center
    

    
    