from collections.abc import Callable

from Items.Bullet import Bullet
from Event.CommandStuff.Command import Command
from Libraries.SimplePyGame.Colors import Colors
from Positions import Vec2
from core.GameElements.Paddle import Paddle
from core.GameElements.Systems.BlockSystem import BlockSystem
from core.GameElements.Systems.Items.Gun import Gun

from core.App import AppConfigs as App, WindowConfig as WC


class GunSystem:

    def __init__(self, paddle: Paddle, block_system: BlockSystem, pass_level: Callable):

        self.paddle = paddle
        self.blockSystem = block_system

        self.pass_level = pass_level

        self.add_bullet = Command(self._add_bullet, delay=0.5, ability_canceled_delete=True)
        self.bullets: list[Bullet] = []

        self.Guns = [
            Gun((-100, 0), (20, 50), Colors.BLACK, self.paddle,
                lambda: (self.paddle.hitbox.right + 10), is_right=True, enable=False, add_bullet=self.add_bullet),
            Gun((-100, 0), (20, 50), Colors.BLACK, self.paddle,
                lambda: (self.paddle.hitbox.left - 10), is_right=False, enable=False, add_bullet=self.add_bullet),
        ]

        self.disable_gun = Command(self._disable_gun, delay=6)

    def _add_bullet(self, pos: Vec2):
        self.bullets.append(Bullet(pos, (10, 20), Colors.BLACK))


    @staticmethod
    def _disable_gun(gun: Gun):
        gun.disable()

    def activate_gun(self):
        for gun in self.Guns[:]:
            if gun.is_disabled:
                # gun.enable = True
                gun.enable()
                self.disable_gun.create(gun).invoke()
                break

    def update(self):
        for gun in self.Guns[:]:
            gun.update()

        for bullet in self.bullets[:]:
            bullet.update()

            if bullet.hitbox.bottom < 0:
                self.bullets.remove(bullet)

            collision_id = bullet.hitbox.collidelist(self.blockSystem.blocks)
            if collision_id != -1:
                self.bullets.remove(bullet)

                block = self.blockSystem.Blocks[collision_id]
                block.hp -= 1

                if block.is_dead:
                    App.sfx.pos_play("explosion", bullet.pos.x)
                    self.blockSystem.kill(collision_id)
                    self.paddle.add_score(5)

                    if len(self.blockSystem.blocks) == 0:
                        self.pass_level()

                else:
                    self.paddle.add_score(3)
                    # App.sfx.pos_play("ball hit", bullet.pos.x)
                    self.blockSystem.BonusSystem.spawn(block.center, 0.1)




    def draw(self):
        for gun in self.Guns[:]:
            gun.draw()

        for bullet in self.bullets[:]:
            bullet.draw()


def main():
    pass


if __name__ == "__main__":
    main()
