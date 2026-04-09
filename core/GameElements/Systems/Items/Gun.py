from Event.CommandStuff.Command import Command
from Libraries.Animations.Functions.Lerp import lerp
from Libraries.SimplePyGame.SDL2.UI.Rectangle import Rectangle
from core.GameElements.Paddle import Paddle

from core.App import AppConfigs as App, WindowConfig as WC


class Gun(Rectangle):
    class Default:
        VELOCITY = -3

    def __init__(self, pos, size, color, paddle: Paddle, target, is_right: bool, add_bullet: Command, remder=None,
                 enable: bool = False):
        super().__init__(pos, size, color, remder)

        self.add_bullet = add_bullet.create(funcs_args=[self.get_pos])

        self.paddle = paddle
        self.target = target

        self.__enable = enable
        self.is_falling = False
        self.velocity = Gun.Default.VELOCITY
        self.Gravity = 10

        self.movement_x = self.movement_right if is_right else self.movement_left

    def get_pos(self):
        return self.hitbox.center

    def enable(self):
        self.__enable = True
        self.add_bullet.invoke(loops=0)

    def disable(self):
        self.__enable = False
        self.is_falling = True
        self.velocity = Gun.Default.VELOCITY
        self.add_bullet.cancel()

    @property
    def is_disabled(self) -> bool:
        return not self.__enable

    def movement_left(self):
        self.hitbox.bottom = self.paddle.hitbox.bottom
        self.hitbox.right = lerp(self.hitbox.right, self.target(), 0.3)

    def movement_right(self):
        self.hitbox.bottom = self.paddle.hitbox.bottom
        self.hitbox.left = lerp(self.hitbox.left, self.target(), 0.3)

    def falling(self):

        self.hitbox.y += self.velocity
        self.velocity += self.Gravity * App.dt

        if self.hitbox.top > WC.H:
            self.is_falling = False

    def update(self):

        if self.__enable:
            self.movement_x()
            self.hitbox.bottom = self.paddle.hitbox.bottom
        elif self.is_falling:
            self.falling()


def main():
    pass


if __name__ == "__main__":
    main()
