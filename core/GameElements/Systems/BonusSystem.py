from pygame._sdl2.video import Renderer

from Libraries.Python.Command import Command
from Libraries.Python.Mixin import InspectorMixin
from Libraries.SimplePyGame.Positions import Vec2
from core.App import AppConfigs as App
from core.GameElements.Paddle import Paddle
from core.GameElements.Systems.Items.Bonus.Bonus import Bonus
from core.GameElements.Systems.Items.Bonus.Bonuses import Bonuses

from random import random, choice


class BonusSystem:
    class Types(InspectorMixin):
        WIDE_PADDLE = 0
        SPEED_BALL = 1

    def __init__(self, paddle: Paddle, render: Renderer = None):

        self.render = render if render else App.Screen.render

        self.Bonuses: list[Bonus] = []

        self.paddle = paddle

        self.Command_Wide_Paddle = Command(self.paddle.expand, 10)
        self.Command_Speed_Ball = Command(self.check2)

    def add_bonus(self, bonus: Bonus):
        self.Bonuses.append(bonus)

    def check1(self):
        print("WIDE_PADDLE")

    def check2(self):
        print("SPEED_BALL")

    def spawn(self, pos: Vec2):

        if random() < 0.5:
            type_bonus = choice(BonusSystem.Types.get_all_values())
            self.add(pos, type_bonus)

    def add(self, pos: Vec2, type: Types | int):

        bonus: Bonus

        match type:
            case BonusSystem.Types.WIDE_PADDLE:
                bonus = Bonuses.wide_paddle(pos, self.Command_Wide_Paddle)

            case BonusSystem.Types.SPEED_BALL:
                bonus = Bonuses.speed_ball(pos, self.Command_Speed_Ball)

            case _:
                raise TypeError("Bonus type not supported")

        self.Bonuses.append(bonus)

    def is_collided_with_paddle(self, bonus: Bonus) -> bool:
        return self.paddle.hitbox.colliderect(bonus.hitbox)

    def update(self):

        for bonus in self.Bonuses:
            bonus.update()

            if self.is_collided_with_paddle(bonus):
                bonus.Command()
                self.Bonuses.remove(bonus)

    def cast_shadows(self):
        for bonus in self.Bonuses:
            bonus.cast_shadow()

    def draw(self):
        for bonus in self.Bonuses:
            bonus.draw()


def main():
    pass


if __name__ == "__main__":
    main()
