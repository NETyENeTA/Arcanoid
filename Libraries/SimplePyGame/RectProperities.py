from Positions import Vec2
from pygame import Rect as PyGameRect


class RectFunctions:

    @staticmethod
    def is_get_in(rect: PyGameRect, pos: Vec2) -> bool:
        return rect.collidepoint(pos.xy)

    # @staticmethod
    # def is_inside(rect: tuple[int, int] | tuple[float, float], size: tuple[int, int] | tuple[float, float],
    #               current: Vec2) -> bool:
    #     return (rect[0] <= current.x <= rect.x + size.x and
    #             rect.y <= current.y <= rect.y + size.y)

    @staticmethod
    def is_inner_in(rect: Vec2, size: Vec2, current: Vec2) -> bool:
        return (rect.x <= current.x <= rect.x + size.x and
                rect.y <= current.y <= rect.y + size.y)


def main():
    pass


if __name__ == "__main__":
    main()
