from Libraries.Animations.Functions.Lerp import lerp
from Libraries.SimplePyGame.SDL2.UI.Rectangle import Rectangle
from core.GameElements.Paddle import Paddle

from core.App import AppConfigs as App, WindowConfig as WC


class Gun(Rectangle):
    class Default:
        VELOCITY = -3

    def __init__(self, pos, size, color, paddle: Paddle, target, is_right: bool, remder=None, enable: bool = False):
        super().__init__(pos, size, color, remder)

        self.paddle = paddle
        self.target = target

        self.enable = enable
        self.is_falling = False
        self.velocity = Gun.Default.VELOCITY
        self.Gravity = 10

        self.movement_x = self.movement_right if is_right else self.movement_left

    def disable(self):
        self.enable = False
        self.is_falling = True
        self.velocity = Gun.Default.VELOCITY

    @property
    def is_disabled(self) -> bool:
        return not self.enable

    def movement_left(self):
        self.hitbox.bottom = self.paddle.hitbox.bottom
        self.hitbox.right = lerp(self.hitbox.right, self.target(), 0.3)

    def movement_right(self):
        self.hitbox.bottom = self.paddle.hitbox.bottom
        self.hitbox.left = lerp(self.hitbox.left, self.target(), 0.3)

    def falling(self):

        self.hitbox.y += self.velocity
        self.velocity += self.Gravity * App.dt

        # print(self.velocity, self.velocity * App.dt)

        if self.hitbox.top > WC.H:
            self.is_falling = False

    def update(self):

        if self.enable:
            self.movement_x()
            self.hitbox.bottom = self.paddle.hitbox.bottom
        elif self.is_falling:
            self.falling()


def main():
    pass


if __name__ == "__main__":
    main()
