from Positions import Vec2
from Libraries.SimplePyGame.SDL2.UI.Rectangle import Rectangle

from core.App import AppConfigs as App


class Bullet(Rectangle):

    def __init__(self, pos, size, color, remder=None):
        super().__init__(pos, size, color, remder)

        self.speed = Vec2(0, -5)
        self.movement = Vec2(20, 100)

    def update(self):
        self.hitbox.y += self.movement.y * self.speed.y * App.dt


def main():
    pass


if __name__ == "__main__":
    main()
