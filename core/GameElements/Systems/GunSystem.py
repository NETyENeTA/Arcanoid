from Libraries.Python.Command import Command
from Libraries.SimplePyGame.Colors import Colors
from core.GameElements.Paddle import Paddle
from core.GameElements.Systems.Items.Gun import Gun


class GunSystem:

    def __init__(self, paddle: Paddle):

        self.paddle = paddle

        self.Guns = [
            Gun((-100, 0), (20, 50), Colors.BLACK, self.paddle,
                lambda: (self.paddle.hitbox.right + 10), is_right=True, enable=False),
            Gun((-100, 0), (20, 50), Colors.BLACK, self.paddle,
                lambda: (self.paddle.hitbox.left - 10), is_right=False, enable=False)
        ]

        self.disable_gun = Command(self._disable_gun, delay=5)

    def _disable_gun(self, gun: Gun):
        gun.disable()

    def activate_gun(self):

        for gun in self.Guns:
            if gun.is_disabled:
                gun.enable = True
                self.disable_gun.args = [gun]
                self.disable_gun.invoke()
                break

    def update(self):

        for gun in self.Guns:
            gun.update()

    def draw(self):
        for gun in self.Guns:
            gun.draw()


def main():
    pass


if __name__ == "__main__":
    main()
