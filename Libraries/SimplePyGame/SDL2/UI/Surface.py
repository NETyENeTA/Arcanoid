from pygame import Rect
from pygame._sdl2 import Texture, Renderer

from Positions import Vec2
from core.App import AppConfigs as App


class Surface:
    def __init__(self, size: Vec2 | tuple[int, int], pos: Vec2 | tuple[int, int] | tuple[float, float] = Vec2.Zero,
                 render: Renderer = None):
        self.render: Renderer = render if render else App.Screen.render
        self.size = size.xy if isinstance(size, Vec2) else size
        # Создаем текстуру-холст. target=True позволяет на ней рисовать
        self.texture = Texture(self.render, size=self.size, target=True)
        self.texture.blend_mode = 1

        # Rect для управления положением на экране
        self.rect = Rect(pos.xy if isinstance(pos, Vec2) else pos, size)

    class _CaptureContext:
        """Вспомогательный класс для переключения цели рендеринга"""

        def __init__(self, parent):
            self.parent = parent

        def __enter__(self):
            self.parent.render.target = self.parent.texture

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.parent.render.target = None

    def capture(self):
        """Контекстный менеджер: всё рисование через self.render внутри 'with' пойдет на этот холст"""
        return self._CaptureContext(self)

    def clear(self, color=(0, 0, 0, 0)):
        """Очищает поверхность заданным цветом"""
        with self.capture():
            self.render.draw_color = color
            self.render.clear()

    def draw(self):
        """Рисует накопленный результат на основной экран"""
        # SDL2 Renderer рисует текстуру в область, указанную в rect
        self.texture.draw(dstrect=self.rect)

    @property
    def alpha(self):
        return self.texture.alpha

    @alpha.setter
    def alpha(self, value: int):
        """Общая прозрачность всего холста (0-255)"""
        self.texture.alpha = max(0, min(255, int(value)))


def main():
    pass


if __name__ == "__main__":
    main()
