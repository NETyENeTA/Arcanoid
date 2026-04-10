from UI.Surface import Surface, Renderer, Vec2, Rect


class ScaleSurface(Surface):
    def __init__(self, size: Vec2 | tuple[int, int], pos: Vec2 | tuple[int, int] | tuple[float, float] = Vec2.Zero,
                 render: Renderer = None, scale: float = 1.0):
        self.scale = scale
        self.display_size = size
        # Рассчитываем уменьшенный размер для внутренней текстуры
        self.internal_size = (int(size[0] / scale), int(size[1] / scale))

        # Вызываем конструктор родителя с уменьшенным размером
        super().__init__(self.internal_size, pos, render)

        # Переопределяем rect, чтобы он соответствовал экранному размеру, а не размеру текстуры
        self.rect = Rect((0, 0), self.display_size)

    def draw(self):
        """Рисует текстуру, растягивая её до размеров self.rect"""
        # При отрисовке маленькая текстура автоматически растянется под размер rect
        self.texture.draw(dstrect=self.rect)


def main():
    pass


if __name__ == "__main__":
    main()
